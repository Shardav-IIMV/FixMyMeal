"""FixMyMeal - Transparent food quality tracking for college hostel messes."""

import streamlit as st
from datetime import datetime
from models import Issue
from data import get_today_menu, get_mock_issues
from gemini_service import validate_api_key, analyze_complaint
from utils import format_date, format_datetime, get_severity_color, get_category_emoji, validate_complaint


# Page configuration
st.set_page_config(
    page_title="FixMyMeal",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS - Theme aware styling
st.markdown("""
    <style>
    .main {
        padding: 0;
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .header h1 {
        margin: 0;
        font-size: 2.5em;
    }
    .header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.9;
    }
    /* Issue cards - use borders instead of light backgrounds */
    .issue-card {
        border-left: 4px solid #667eea;
        border-top: 1px solid #667eea;
        border-right: 1px solid #667eea;
        border-bottom: 1px solid #667eea;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        opacity: 0.95;
    }
    /* Severity labels - use colors with good contrast in both themes */
    .severity-critical {
        color: #e74c3c;
        font-weight: bold;
    }
    .severity-high {
        color: #e67e22;
        font-weight: bold;
    }
    .severity-medium {
        color: #f39c12;
        font-weight: bold;
    }
    .severity-low {
        color: #27ae60;
        font-weight: bold;
    }
    /* Menu items - no background, inherit theme */
    .menu-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        font-size: 0.9em;
        border-left: 3px solid #667eea;
        padding-left: 12px;
    }
    /* AI analysis box - use border styling instead of colored background */
    .ai-analysis-box {
        padding: 15px;
        border-left: 4px solid #0099cc;
        border-top: 1px solid #0099cc;
        border-right: 1px solid #0099cc;
        border-bottom: 1px solid #0099cc;
        border-radius: 5px;
        margin: 10px 0;
        opacity: 0.95;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state."""
    if "issues" not in st.session_state:
        st.session_state.issues = get_mock_issues()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    
    if "pending_issue" not in st.session_state:
        st.session_state.pending_issue = None
    
    if "selected_issue_id" not in st.session_state:
        st.session_state.selected_issue_id = None


def show_home_page():
    """Display the home page."""
    st.markdown("""
    <div class="header">
        <h1>🍽️ FixMyMeal</h1>
        <p>Transparent food quality tracking for your hostel mess.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Report Issue Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Report an Issue", use_container_width=True, key="home_report_btn"):
            st.session_state.current_page = "report"
            st.rerun()
    
    st.divider()
    
    # Today's Menu Section
    st.subheader("📋 Today's Menu")
    today_menu = get_today_menu()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Breakfast**")
        for item in today_menu.get("breakfast", []):
            st.markdown(f'<div class="menu-item">• {item}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Lunch**")
        for item in today_menu.get("lunch", []):
            st.markdown(f'<div class="menu-item">• {item}</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("**Snacks**")
        for item in today_menu.get("snacks", []):
            st.markdown(f'<div class="menu-item">• {item}</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown("**Dinner**")
        for item in today_menu.get("dinner", []):
            st.markdown(f'<div class="menu-item">• {item}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Recent Issues Section
    st.subheader("📢 Recent Issues")
    
    if st.session_state.issues:
        # Sort by most recent first
        sorted_issues = sorted(st.session_state.issues, key=lambda x: x.created_at, reverse=True)[:5]
        
        for issue in sorted_issues:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div class="issue-card">
                        <strong>{issue.summary}</strong><br/>
                        {get_category_emoji(issue.category or 'Other')} {issue.category or 'Other'} | 
                        {get_severity_color(issue.severity or 'Low')} {issue.severity or 'Low'} | 
                        🍽️ {issue.meal} | 📅 {format_date(issue.date)}
                        {' | 📸 Evidence attached' if issue.has_evidence else ''}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("View", key=f"view_{issue.id}", use_container_width=True):
                        st.session_state.selected_issue_id = issue.id
                        st.session_state.current_page = "detail"
                        st.rerun()
    else:
        st.info("No issues reported yet. Be the first to help improve our mess!")


def show_report_page():
    """Display the report issue page."""
    st.title("📝 Report an Issue")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown("Help us improve the mess quality by reporting your experience.")
    
    # Check if we have an analysis result to display
    if st.session_state.analysis_result and st.session_state.pending_issue:
        show_analysis_review()
    else:
        show_report_form()


def show_report_form():
    """Display the complaint form."""
    st.subheader("Your Complaint")
    
    # Meal selection
    meal = st.selectbox(
        "Which meal was this about?",
        ["Breakfast", "Lunch", "Snacks", "Dinner"],
        key="meal_select"
    )
    
    # Complaint description
    description = st.text_area(
        "Describe the issue in your own words (be as specific as possible)",
        placeholder="E.g., The dal had a strange taste and looked discolored. There might have been something in it.",
        key="complaint_text"
    )
    
    # Image upload (optional)
    st.markdown("**Evidence (optional)**")
    uploaded_image = st.file_uploader(
        "Upload a photo if you have evidence",
        type=["jpg", "jpeg", "png"],
        key="image_upload"
    )
    
    # Analyse button
    if st.button("🔍 Analyse Report", use_container_width=True, key="analyse_btn"):
        # Validate input
        is_valid, error_msg = validate_complaint(description, meal)
        if not is_valid:
            st.error(error_msg)
        elif not validate_api_key():
            st.error(
                "⚠️ Gemini API key not configured. "
                "Please add GEMINI_API_KEY to Streamlit Secrets."
            )
        else:
            with st.spinner("🤖 AI is analyzing your report..."):
                image_data = None
                if uploaded_image:
                    image_data = uploaded_image.getvalue()
                
                result = analyze_complaint(description, meal, image_data)
            
            if result.get("error"):
                st.error(f"❌ {result.get('message', 'Unknown error')}")
            else:
                # Store analysis and pending issue
                st.session_state.analysis_result = result
                st.session_state.pending_issue = {
                    "description": description,
                    "meal": meal,
                    "image": image_data,
                }
                st.rerun()


def show_analysis_review():
    """Display the AI analysis for review."""
    st.subheader("✅ AI-Assisted Analysis")
    
    analysis = st.session_state.analysis_result
    pending = st.session_state.pending_issue
    
    # Show original complaint
    st.markdown("### Your Complaint")
    st.text(pending["description"])
    
    st.divider()
    
    # Show AI analysis
    st.markdown("### AI-Generated Classification")
    st.markdown(f"""
    <div class="ai-analysis-box">
        <p><strong>Category:</strong> {get_category_emoji(analysis['category'])} {analysis['category']}</p>
        <p><strong>Severity:</strong> {get_severity_color(analysis['severity'])} {analysis['severity']}</p>
        <p><strong>Summary:</strong> {analysis['summary']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show image if provided
    if pending["image"]:
        st.markdown("### Evidence Photo")
        st.image(pending["image"], caption="Your uploaded evidence")
    
    st.markdown("### What happens next?")
    st.markdown("""
    - Your issue will be added to the issue feed
    - The hostel management can view and track the issue
    - Other students will see aggregated issues by category
    """)
    
    # Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✏️ Edit / Analyse Again", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.pending_issue = None
            st.rerun()
    
    with col2:
        if st.button("✅ Confirm & Submit", use_container_width=True):
            # Create issue
            new_issue = Issue(
                id=str(len(st.session_state.issues) + 1),
                description=pending["description"],
                meal=pending["meal"],
                date=datetime.now().date().isoformat(),
                created_at=datetime.now(),
                status="Reported",
                image=pending["image"],
                category=analysis["category"],
                severity=analysis["severity"],
                summary=analysis["summary"],
            )
            
            # Add to issues list
            st.session_state.issues.append(new_issue)
            
            # Clear analysis
            st.session_state.analysis_result = None
            st.session_state.pending_issue = None
            
            st.success("✅ Thank you! Your issue has been submitted.")
            st.balloons()
            
            # Redirect to home
            import time
            time.sleep(2)
            st.session_state.current_page = "home"
            st.rerun()


def show_issues_page():
    """Display the issues feed page."""
    st.title("📢 Issue Feed")
    
    # Back button
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.markdown(f"**Total issues:** {len(st.session_state.issues)}")
    
    # Filters and sorting
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "Hygiene", "Taste", "Quantity", "Timing", "Other"],
            key="category_filter"
        )
    
    with col2:
        sort_order = st.selectbox(
            "Sort by",
            ["Most Recent", "Oldest"],
            key="sort_order"
        )
    
    with col3:
        st.empty()  # Just for spacing
    
    st.divider()
    
    # Filter issues
    filtered_issues = st.session_state.issues
    if category_filter != "All":
        filtered_issues = [i for i in filtered_issues if i.category == category_filter]
    
    # Sort issues
    if sort_order == "Most Recent":
        filtered_issues = sorted(filtered_issues, key=lambda x: x.created_at, reverse=True)
    else:
        filtered_issues = sorted(filtered_issues, key=lambda x: x.created_at)
    
    # Display issues
    if filtered_issues:
        for issue in filtered_issues:
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div class="issue-card">
                        <strong>{issue.summary}</strong><br/>
                        {get_category_emoji(issue.category or 'Other')} {issue.category or 'Other'} | 
                        {get_severity_color(issue.severity or 'Low')} <span class="severity-{issue.severity.lower()}">{issue.severity or 'Low'}</span> | 
                        🍽️ {issue.meal} | 📅 {format_date(issue.date)}
                        {' | 📸 Evidence attached' if issue.has_evidence else ''}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("View", key=f"view_issue_{issue.id}", use_container_width=True):
                        st.session_state.selected_issue_id = issue.id
                        st.session_state.current_page = "detail"
                        st.rerun()
    else:
        st.info("No issues found in this category.")


def show_detail_page():
    """Display the issue detail page."""
    issue_id = st.session_state.selected_issue_id
    issue = next((i for i in st.session_state.issues if i.id == issue_id), None)
    
    if not issue:
        st.error("Issue not found.")
        if st.button("← Back to Issues"):
            st.session_state.current_page = "home"
            st.rerun()
        return
    
    # Back button
    if st.button("← Back to Issues"):
        st.session_state.current_page = "home"
        st.rerun()
    
    st.title(issue.summary)
    
    # Status and metadata
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Category", f"{get_category_emoji(issue.category)} {issue.category}")
    with col2:
        st.metric("Severity", f"{get_severity_color(issue.severity)} {issue.severity}")
    with col3:
        st.metric("Meal", issue.meal)
    with col4:
        st.metric("Date", format_date(issue.date))
    
    st.divider()
    
    # Student's original complaint
    st.subheader("📝 Student's Complaint")
    st.text(issue.description)
    
    st.divider()
    
    # Image if available
    if issue.image:
        st.subheader("📸 Evidence Photo")
        st.image(issue.image, caption="Student provided evidence")
        st.divider()
    
    # AI analysis
    st.subheader("✅ AI-Assisted Classification")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Category:** {issue.category}")
    with col2:
        st.warning(f"**Severity:** {issue.severity}")
    
    st.markdown(f"**Summary:** {issue.summary}")
    
    st.divider()
    
    # Status
    st.subheader("Status")
    st.info(f"Current Status: **{issue.status}**")
    
    st.markdown("*Resolution tracking will be available in a future version.*")


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Navigation
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "report":
        show_report_page()
    elif st.session_state.current_page == "issues":
        show_issues_page()
    elif st.session_state.current_page == "detail":
        show_detail_page()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
        
        if st.button("📢 View All Issues", use_container_width=True):
            st.session_state.current_page = "issues"
            st.rerun()
        
        if st.button("📝 Report Issue", use_container_width=True):
            st.session_state.current_page = "report"
            st.rerun()
        
        st.divider()
        
        st.markdown("### About")
        st.markdown(
            "FixMyMeal helps students report food quality issues with AI-powered analysis."
        )
        
        st.divider()
        
        st.markdown("### API Status")
        if validate_api_key():
            st.success("✅ Gemini API configured")
        else:
            st.error("❌ Gemini API not configured")


if __name__ == "__main__":
    main()
