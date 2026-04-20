from guardrails_eval import check_safety
import streamlit as st

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    # Check safety using AI (OpenAI)
    result = check_safety(resume_text)

    if result['safe']:
        confidence = result.get('confidence', 0)
        st.success(f"✅ Resume passed AI safety check! (Confidence: {confidence:.1%})")
        # Continue processing...
    else:
        st.error(f"❌ Safety violation: {result['reason']}")
        if result.get('categories'):
            st.warning(f"Categories: {', '.join(result['categories'])}")
        st.stop()