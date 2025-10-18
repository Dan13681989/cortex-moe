import streamlit as st
import random
from datetime import datetime
import json

# Configure the page
st.set_page_config(
    page_title="Cortex-MoE: Mixture of Experts",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'usage_stats' not in st.session_state:
    st.session_state.usage_stats = {
        'creative_count': 0,
        'logic_count': 0,
        'total_queries': 0
    }

# Expert Systems
class CreativeExpert:
    def __init__(self):
        self.name = "🎨 Creative Expert"
        self.specialties = ["writing", "storytelling", "marketing", "content creation", "branding"]
    
    def respond(self, query):
        creative_responses = [
            f"✨ Let me craft a compelling narrative for: '{query}'. Here's a creative approach...",
            f"🎭 From a storytelling perspective, '{query}' suggests these creative possibilities...",
            f"📝 For '{query}', I recommend this marketing angle with emotional appeal...",
            f"💡 Creative insight: '{query}' could be transformed through these innovative concepts..."
        ]
        return random.choice(creative_responses)

class LogicExpert:
    def __init__(self):
        self.name = "🔍 Logic Expert"
        self.specialties = ["analysis", "reasoning", "research", "problem-solving", "data"]
    
    def respond(self, query):
        logic_responses = [
            f"🔬 Analyzing '{query}' logically, I identify these key factors and relationships...",
            f"📊 Based on systematic analysis of '{query}', the evidence suggests...",
            f"💭 Logical reasoning for '{query}' reveals these causal relationships...",
            f"📈 Data-driven perspective on '{query}' indicates these patterns and conclusions..."
        ]
        return random.choice(logic_responses)

# Router System
class ExpertRouter:
    def __init__(self):
        self.creative_expert = CreativeExpert()
        self.logic_expert = LogicExpert()
        self.creative_keywords = ['write', 'story', 'creative', 'marketing', 'content', 'brand', 'design', 'art']
        self.logic_keywords = ['analyze', 'solve', 'research', 'data', 'logic', 'reason', 'problem', 'how']
    
    def route_question(self, query):
        query_lower = query.lower()
        
        # Count keyword matches
        creative_score = sum(1 for word in self.creative_keywords if word in query_lower)
        logic_score = sum(1 for word in self.logic_keywords if word in query_lower)
        
        if creative_score > logic_score:
            st.session_state.usage_stats['creative_count'] += 1
            return self.creative_expert, self.creative_expert.respond(query)
        else:
            st.session_state.usage_stats['logic_count'] += 1
            return self.logic_expert, self.logic_expert.respond(query)

# Initialize router
router = ExpertRouter()

# UI Components
def main():
    st.title("🧠 Cortex-MoE: Mixture of Experts")
    st.markdown("### Intelligent Expert Routing System")
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Analytics")
        st.metric("Total Queries", st.session_state.usage_stats['total_queries'])
        st.metric("Creative Expert", st.session_state.usage_stats['creative_count'])
        st.metric("Logic Expert", st.session_state.usage_stats['logic_count'])
        
        st.header("🎯 Expert Specialties")
        st.info("**🎨 Creative Expert**: Writing, storytelling, marketing, content")
        st.info("**🔍 Logic Expert**: Analysis, reasoning, research, problem-solving")
        
        if st.button("Clear History"):
            st.session_state.conversation_history = []
            st.rerun()
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Ask Anything")
        user_query = st.text_input("Enter your question:", placeholder="e.g., 'Help me write a marketing story' or 'Analyze this data pattern'")
        
        if st.button("Get Expert Response") and user_query:
            with st.spinner("Routing to best expert..."):
                # Route to expert
                expert, response = router.route_question(user_query)
                st.session_state.usage_stats['total_queries'] += 1
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'query': user_query,
                    'expert': expert.name,
                    'response': response
                })
                
                # Display response
                st.success(f"**{expert.name}** responded:")
                st.write(response)
        
        # Conversation history
        if st.session_state.conversation_history:
            st.subheader("📜 Conversation History")
            for i, conv in enumerate(reversed(st.session_state.conversation_history[-5:]), 1):
                with st.expander(f"{conv['timestamp']} - {conv['expert']}"):
                    st.write(f"**Q:** {conv['query']}")
                    st.write(f"**A:** {conv['response']}")
    
    with col2:
        st.subheader("🚀 Quick Examples")
        examples = [
            "Write a creative marketing story",
            "Analyze this business problem logically",
            "Help me design a brand strategy",
            "Research methodology for user data"
        ]
        
        for example in examples:
            if st.button(example, key=example):
                st.session_state.user_query = example
                st.rerun()

if __name__ == "__main__":
    main()
