import streamlit as st


# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'game_type' not in st.session_state:
    st.session_state.game_type = None
if 'num_players' not in st.session_state:
    st.session_state.num_players = 2
if 'player_names' not in st.session_state:
    st.session_state.player_names = []
if 'player_scores' not in st.session_state:
    st.session_state.player_scores = {}
# Brawl-specific states
if 'brawl_grid' not in st.session_state:
    st.session_state.brawl_grid = None
if 'brawl_markers' not in st.session_state:
    st.session_state.brawl_markers = []
if 'table_rows' not in st.session_state:
    st.session_state.table_rows = 3
if 'table_cols' not in st.session_state:
    st.session_state.table_cols = 3


# Navigation functions
def go_to_rummy():
    st.session_state.page = 'rummy'


def go_to_brawl():
    st.session_state.page = 'brawl'


def go_to_normal_game():
    st.session_state.game_type = 'normal'
    st.session_state.page = 'normal_game'
    st.session_state.num_rounds = 5


def go_to_seven_game():
    st.session_state.game_type = '7_game'
    st.session_state.page = '7_game'
    st.session_state.num_rounds = 7


def go_home():
    st.session_state.page = 'home'
    st.session_state.game_type = None
    st.session_state.player_scores = {}
    st.session_state.brawl_grid = None


def reset_scores():
    st.session_state.player_scores = {}


def reset_brawl():
    st.session_state.brawl_grid = None
    st.session_state.brawl_markers = []


# Set page config for wide layout with mobile viewport
st.set_page_config(
    layout="wide", 
    page_title="Game Score Tracker",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for mobile responsiveness
st.markdown("""
<style>
    /* Mobile viewport fix */
    @viewport {
        width: device-width;
        zoom: 1.0;
    }
    
    /* Compact number inputs - touch friendly */
    div[data-testid="stNumberInput"] > div > div > input {
        font-size: 20px !important;
        padding: 12px !important;
        height: 50px !important;
        text-align: center !important;
        min-height: 44px !important;
        -webkit-appearance: none !important;
        border-radius: 8px !important;
    }
    
    /* Text inputs styling */
    div[data-testid="stTextInput"] > div > div > input {
        font-size: 18px !important;
        padding: 10px !important;
        text-align: center !important;
        text-transform: uppercase !important;
        font-weight: bold !important;
    }
    
    /* Hide up/down arrows */
    div[data-testid="stNumberInput"] button {
        display: none !important;
    }
    
    /* Better touch targets for buttons */
    button {
        min-height: 44px !important;
        font-size: 16px !important;
        padding: 12px 20px !important;
        touch-action: manipulation !important;
    }
    
    /* Prevent text selection on double tap */
    * {
        -webkit-tap-highlight-color: transparent;
        -webkit-touch-callout: none;
        user-select: none;
    }
    
    /* Allow text selection in inputs */
    input, textarea {
        user-select: text !important;
        -webkit-user-select: text !important;
    }
    
    /* Reduce spacing on mobile */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* Compact dividers */
    hr {
        margin: 0.5rem 0 !important;
    }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 24px !important;
        }
        
        h2 {
            font-size: 20px !important;
        }
        
        h3 {
            font-size: 18px !important;
        }
        
        .stColumns {
            flex-direction: column !important;
        }
        
        div[data-testid="stNumberInput"] {
            width: 100% !important;
        }
        
        button {
            min-height: 48px !important;
            font-size: 18px !important;
        }
        
        .element-container {
            margin-bottom: 0.5rem !important;
        }
    }
    
    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1024px) {
        .block-container {
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    }
    
    /* Prevent zoom on input focus (iOS) */
    @media screen and (-webkit-min-device-pixel-ratio: 0) {
        input, select, textarea {
            font-size: 16px !important;
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
        -webkit-overflow-scrolling: touch;
    }
    
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(136, 136, 136, 0.5);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)


# Homepage
if st.session_state.page == 'home':
    st.title("🎮 Game Score Tracker")
    st.write("Select a game to start:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🃏 Rummy", on_click=go_to_rummy, use_container_width=True)
    with col2:
        st.button("⚔️ Brawl", on_click=go_to_brawl, use_container_width=True)


# Rummy selection page
elif st.session_state.page == 'rummy':
    st.title("🃏 Rummy Game")
    st.write("Choose game type:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Normal Game", on_click=go_to_normal_game, use_container_width=True)
    with col2:
        st.button("7 Game", on_click=go_to_seven_game, use_container_width=True)
    
    st.button("← Back to Home", on_click=go_home)


# Normal Game page - UPDATED WITH ADD ROUND FEATURE
elif st.session_state.page == 'normal_game':
    st.title("🃏 Rummy - Normal Game")
    
    num_players = st.number_input("Number of Players:", min_value=2, max_value=10, value=st.session_state.num_players, step=1)
    st.session_state.num_players = num_players
    
    st.subheader("Enter Player Names:")
    cols_count = min(num_players, 3) if num_players <= 4 else min(num_players, 4)
    cols = st.columns(cols_count)
    player_names = []
    
    for i in range(num_players):
        with cols[i % cols_count]:
            default_name = st.session_state.player_names[i] if i < len(st.session_state.player_names) else f"Player {i+1}"
            name = st.text_input(f"Player {i+1}:", value=default_name, key=f"player_{i}")
            player_names.append(name)
    
    st.session_state.player_names = player_names
    
    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.player_scores = {name: [0] * st.session_state.num_rounds for name in player_names}
        st.rerun()
    
    if st.session_state.player_scores:
        st.divider()
        
        # Add round button at the top
        col_header1, col_header2 = st.columns([3, 1])
        with col_header1:
            st.subheader("📝 Scores")
        with col_header2:
            if st.button("➕ Add Round", use_container_width=True):
                # Add a new round (append 0 to each player's score list)
                for player in st.session_state.player_scores:
                    st.session_state.player_scores[player].append(0)
                st.session_state.num_rounds = len(st.session_state.player_scores[player_names[0]])
                st.rerun()
        
        # Get current number of rounds from actual data
        current_rounds = len(st.session_state.player_scores[player_names[0]])
        
        use_mobile_layout = num_players > 3
        
        if use_mobile_layout:
            for player in player_names:
                with st.expander(f"**{player}**", expanded=False):
                    if player not in st.session_state.player_scores:
                        st.session_state.player_scores[player] = [0] * current_rounds
                    
                    for round_idx in range(current_rounds):
                        if round_idx == 0:
                            prev_total = 0
                        else:
                            prev_total = sum(st.session_state.player_scores[player][:round_idx])
                        
                        st.markdown(f"<div style='font-size: 14px; color: #999; margin: 8px 0;'>Round {round_idx + 1}</div>", unsafe_allow_html=True)
                        
                        cols_inner = st.columns([2, 0.5, 2])
                        
                        with cols_inner[0]:
                            st.markdown(f"""
                                <div style='
                                    padding: 12px; 
                                    text-align: center; 
                                    font-size: 20px; 
                                    font-weight: 600;
                                    border: 2px solid #444; 
                                    border-radius: 8px;
                                    background-color: #1a1a1a;
                                    color: #ddd;
                                    min-height: 50px;
                                    line-height: 26px;
                                '>{prev_total}</div>
                            """, unsafe_allow_html=True)
                        
                        with cols_inner[1]:
                            st.markdown("<div style='padding: 12px; text-align: center; font-size: 24px; font-weight: bold; color: #4CAF50; line-height: 26px;'>+</div>", unsafe_allow_html=True)
                        
                        with cols_inner[2]:
                            score = st.number_input(
                                f"Round {round_idx + 1}",
                                min_value=0,
                                value=st.session_state.player_scores[player][round_idx],
                                step=1,
                                key=f"score_{player}_{round_idx}",
                                label_visibility="collapsed"
                            )
                            st.session_state.player_scores[player][round_idx] = score
                    
                    total = sum(st.session_state.player_scores[player])
                    st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold; color: #1f77b4; margin-top: 10px;'>Total: {total} pts</div>", unsafe_allow_html=True)
        
        else:
            header_cols_list = []
            for idx in range(num_players):
                if idx > 0:
                    header_cols_list.append(0.05)
                header_cols_list.append(1)
            
            header_cols = st.columns(header_cols_list)
            
            col_index = 0
            for idx, player in enumerate(player_names):
                if idx > 0:
                    with header_cols[col_index]:
                        st.markdown("<div style='border-left: 2px solid #555; height: 100%;'></div>", unsafe_allow_html=True)
                    col_index += 1
                
                with header_cols[col_index]:
                    st.markdown(f"<div style='text-align: center; font-size: 22px; font-weight: bold; color: #1f77b4; padding: 10px;'>{player}</div>", unsafe_allow_html=True)
                col_index += 1
            
            st.markdown("---")
            
            for round_idx in range(current_rounds):
                st.markdown(f"<div style='font-size: 14px; color: #999; margin: 12px 0 8px 0;'>Round {round_idx + 1}</div>", unsafe_allow_html=True)
                
                round_cols = st.columns(header_cols_list)
                
                col_index = 0
                for player_idx, player in enumerate(player_names):
                    if player not in st.session_state.player_scores:
                        st.session_state.player_scores[player] = [0] * current_rounds
                    
                    if player_idx > 0:
                        with round_cols[col_index]:
                            st.markdown("<div style='border-left: 2px solid #555; height: 55px;'></div>", unsafe_allow_html=True)
                        col_index += 1
                    
                    with round_cols[col_index]:
                        if round_idx == 0:
                            prev_total = 0
                        else:
                            prev_total = sum(st.session_state.player_scores[player][:round_idx])
                        
                        cols_inner = st.columns([2, 0.5, 2])
                        
                        with cols_inner[0]:
                            st.markdown(f"""
                                <div style='
                                    padding: 8px; 
                                    text-align: center; 
                                    font-size: 18px; 
                                    font-weight: 600;
                                    border: 1.5px solid #444; 
                                    border-radius: 6px;
                                    background-color: #1a1a1a;
                                    color: #ddd;
                                    height: 45px;
                                    line-height: 29px;
                                '>{prev_total}</div>
                            """, unsafe_allow_html=True)
                        
                        with cols_inner[1]:
                            st.markdown("<div style='padding: 8px; text-align: center; font-size: 20px; font-weight: bold; color: #4CAF50; line-height: 29px;'>+</div>", unsafe_allow_html=True)
                        
                        with cols_inner[2]:
                            score = st.number_input(
                                f"Round {round_idx + 1}",
                                min_value=0,
                                value=st.session_state.player_scores[player][round_idx],
                                step=1,
                                key=f"score_{player}_{round_idx}",
                                label_visibility="collapsed"
                            )
                            st.session_state.player_scores[player][round_idx] = score
                    
                    col_index += 1
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.subheader("🏆 Final Scores")
        standings = {player: sum(scores) for player, scores in st.session_state.player_scores.items()}
        sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
        
        cols_standing = st.columns(min(len(sorted_standings), 3))
        for idx, (player, total_score) in enumerate(sorted_standings):
            with cols_standing[idx % min(len(sorted_standings), 3)]:
                medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx + 1}"
                st.markdown(f"<div style='text-align: center; font-size: 32px;'>{medal}</div>", unsafe_allow_html=True)
                st.metric(label=player, value=f"{total_score} pts")
        
        st.button("🔄 Reset Scores", on_click=reset_scores, use_container_width=True)
    
    st.button("← Back to Rummy Options", on_click=go_to_rummy)


# 7 Game page (similar to Normal Game - keeping previous implementation)
elif st.session_state.page == '7_game':
    st.title("🃏 Rummy - 7 Game")
    
    num_players = st.number_input("Number of Players:", min_value=2, max_value=10, value=st.session_state.num_players, step=1)
    st.session_state.num_players = num_players
    
    st.subheader("Enter Player Names:")
    cols_count = min(num_players, 3) if num_players <= 4 else min(num_players, 4)
    cols = st.columns(cols_count)
    player_names = []
    
    for i in range(num_players):
        with cols[i % cols_count]:
            default_name = st.session_state.player_names[i] if i < len(st.session_state.player_names) else f"Player {i+1}"
            name = st.text_input(f"Player {i+1}:", value=default_name, key=f"player_7_{i}")
            player_names.append(name)
    
    st.session_state.player_names = player_names
    
    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.player_scores = {name: [0] * 7 for name in player_names}
        st.rerun()
    
    if st.session_state.player_scores:
        st.divider()
        st.subheader("📝 Scores")
        
        use_mobile_layout = num_players > 3
        
        if use_mobile_layout:
            for player in player_names:
                with st.expander(f"**{player}**", expanded=False):
                    if player not in st.session_state.player_scores:
                        st.session_state.player_scores[player] = [0] * 7
                    
                    for round_idx in range(7):
                        if round_idx == 0:
                            prev_total = 0
                        else:
                            prev_total = sum(st.session_state.player_scores[player][:round_idx])
                        
                        st.markdown(f"<div style='font-size: 14px; color: #999; margin: 8px 0;'>Round {round_idx + 1}</div>", unsafe_allow_html=True)
                        
                        cols_inner = st.columns([2, 0.5, 2])
                        
                        with cols_inner[0]:
                            st.markdown(f"""
                                <div style='
                                    padding: 12px; 
                                    text-align: center; 
                                    font-size: 20px; 
                                    font-weight: 600;
                                    border: 2px solid #444; 
                                    border-radius: 8px;
                                    background-color: #1a1a1a;
                                    color: #ddd;
                                    min-height: 50px;
                                    line-height: 26px;
                                '>{prev_total}</div>
                            """, unsafe_allow_html=True)
                        
                        with cols_inner[1]:
                            st.markdown("<div style='padding: 12px; text-align: center; font-size: 24px; font-weight: bold; color: #4CAF50; line-height: 26px;'>+</div>", unsafe_allow_html=True)
                        
                        with cols_inner[2]:
                            if round_idx == 6:
                                final_score = st.session_state.player_scores[player][round_idx]
                                st.markdown(f"""
                                    <div style='
                                        padding: 12px; 
                                        text-align: center; 
                                        font-size: 20px; 
                                        font-weight: 600;
                                        border: 2px solid #4CAF50; 
                                        border-radius: 8px;
                                        background-color: #1f2f1f;
                                        color: #4CAF50;
                                        min-height: 50px;
                                        line-height: 26px;
                                    '>{final_score if final_score > 0 else '−'}</div>
                                """, unsafe_allow_html=True)
                            else:
                                score = st.number_input(
                                    f"Round {round_idx + 1}",
                                    min_value=0,
                                    value=st.session_state.player_scores[player][round_idx],
                                    step=1,
                                    key=f"score_{player}_{round_idx}",
                                    label_visibility="collapsed"
                                )
                                st.session_state.player_scores[player][round_idx] = score
                    
                    total = sum(st.session_state.player_scores[player])
                    st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold; color: #1f77b4; margin-top: 10px;'>Total: {total} pts</div>", unsafe_allow_html=True)
        
        else:
            header_cols_list = []
            for idx in range(num_players):
                if idx > 0:
                    header_cols_list.append(0.05)
                header_cols_list.append(1)
            
            header_cols = st.columns(header_cols_list)
            
            col_index = 0
            for idx, player in enumerate(player_names):
                if idx > 0:
                    with header_cols[col_index]:
                        st.markdown("<div style='border-left: 2px solid #555; height: 100%;'></div>", unsafe_allow_html=True)
                    col_index += 1
                
                with header_cols[col_index]:
                    st.markdown(f"<div style='text-align: center; font-size: 22px; font-weight: bold; color: #1f77b4; padding: 10px;'>{player}</div>", unsafe_allow_html=True)
                col_index += 1
            
            st.markdown("---")
            
            for round_idx in range(7):
                st.markdown(f"<div style='font-size: 14px; color: #999; margin: 12px 0 8px 0;'>Round {round_idx + 1}</div>", unsafe_allow_html=True)
                
                round_cols = st.columns(header_cols_list)
                
                col_index = 0
                for player_idx, player in enumerate(player_names):
                    if player not in st.session_state.player_scores:
                        st.session_state.player_scores[player] = [0] * 7
                    
                    if player_idx > 0:
                        with round_cols[col_index]:
                            st.markdown("<div style='border-left: 2px solid #555; height: 55px;'></div>", unsafe_allow_html=True)
                        col_index += 1
                    
                    with round_cols[col_index]:
                        if round_idx == 0:
                            prev_total = 0
                        else:
                            prev_total = sum(st.session_state.player_scores[player][:round_idx])
                        
                        cols_inner = st.columns([2, 0.5, 2])
                        
                        with cols_inner[0]:
                            st.markdown(f"""
                                <div style='
                                    padding: 8px; 
                                    text-align: center; 
                                    font-size: 18px; 
                                    font-weight: 600;
                                    border: 1.5px solid #444; 
                                    border-radius: 6px;
                                    background-color: #1a1a1a;
                                    color: #ddd;
                                    height: 45px;
                                    line-height: 29px;
                                '>{prev_total}</div>
                            """, unsafe_allow_html=True)
                        
                        with cols_inner[1]:
                            st.markdown("<div style='padding: 8px; text-align: center; font-size: 20px; font-weight: bold; color: #4CAF50; line-height: 29px;'>+</div>", unsafe_allow_html=True)
                        
                        with cols_inner[2]:
                            if round_idx == 6:
                                final_score = st.session_state.player_scores[player][round_idx]
                                st.markdown(f"""
                                    <div style='
                                        padding: 8px; 
                                        text-align: center; 
                                        font-size: 18px; 
                                        font-weight: 600;
                                        border: 1.5px solid #4CAF50; 
                                        border-radius: 6px;
                                        background-color: #1f2f1f;
                                        color: #4CAF50;
                                        height: 45px;
                                        line-height: 29px;
                                    '>{final_score if final_score > 0 else '−'}</div>
                                """, unsafe_allow_html=True)
                            else:
                                score = st.number_input(
                                    f"Round {round_idx + 1}",
                                    min_value=0,
                                    value=st.session_state.player_scores[player][round_idx],
                                    step=1,
                                    key=f"score_{player}_{round_idx}",
                                    label_visibility="collapsed"
                                )
                                st.session_state.player_scores[player][round_idx] = score
                    
                    col_index += 1
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.subheader("🏆 Final Scores")
        standings = {player: sum(scores) for player, scores in st.session_state.player_scores.items()}
        sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
        
        cols_standing = st.columns(min(len(sorted_standings), 3))
        for idx, (player, total_score) in enumerate(sorted_standings):
            with cols_standing[idx % min(len(sorted_standings), 3)]:
                medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx + 1}"
                st.markdown(f"<div style='text-align: center; font-size: 32px;'>{medal}</div>", unsafe_allow_html=True)
                st.metric(label=player, value=f"{total_score} pts")
        
        st.button("🔄 Reset Scores", on_click=reset_scores, use_container_width=True)
    
    st.button("← Back to Rummy Options", on_click=go_to_rummy)

# Brawl page - UPDATED WITH CELL BORDERS
elif st.session_state.page == 'brawl':
    st.title("⚔️ Brawl Game")
    
    # Configuration section
    if st.session_state.brawl_grid is None:
        st.subheader("🎯 Setup Game")
        
        # Table dimensions
        col1, col2 = st.columns(2)
        with col1:
            rows = st.number_input("Number of Rows:", min_value=2, max_value=20, value=st.session_state.table_rows, step=1)
            st.session_state.table_rows = rows
        with col2:
            cols_num = st.number_input("Number of Columns:", min_value=2, max_value=20, value=st.session_state.table_cols, step=1)
            st.session_state.table_cols = cols_num
        
        st.markdown("---")
        
        num_markers = st.number_input("Number of Markers:", min_value=2, max_value=10, value=2, step=1)
        
        # Available letters for markers
        available_letters = [chr(i) for i in range(65, 91)]  # A-Z
        
        markers = []
        marker_cols = st.columns(min(num_markers, 5))
        
        for i in range(num_markers):
            with marker_cols[i % 5]:
                # Default selection
                default_marker = st.session_state.brawl_markers[i] if i < len(st.session_state.brawl_markers) else chr(65+i)
                default_index = available_letters.index(default_marker) if default_marker in available_letters else i
                
                marker = st.selectbox(
                    f"Marker {i+1}:",
                    options=available_letters,
                    index=default_index,
                    key=f"marker_{i}"
                )
                markers.append(marker)
        
        st.session_state.brawl_markers = markers
        
        # Start game button
        if st.button("🎮 Start Brawl", type="primary", use_container_width=True):
            # Initialize grid with empty strings
            st.session_state.brawl_grid = [["" for _ in range(st.session_state.table_cols)] for _ in range(st.session_state.table_rows)]
            st.rerun()
    
    else:
        # Game interface
        st.subheader("📊 Brawl Grid")
        
        # Display markers legend
        st.markdown("**Active Markers:**")
        marker_display_cols = st.columns(len(st.session_state.brawl_markers))
        for idx, marker in enumerate(st.session_state.brawl_markers):
            with marker_display_cols[idx]:
                st.markdown(f"<div style='text-align: center; padding: 10px; background-color: #1f77b4; border-radius: 8px; font-size: 20px; font-weight: bold;'>{marker}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Add container with grid styling
        st.markdown("""
        <style>
        /* Grid container styling */
        .grid-container {
            display: grid;
            gap: 0;
            border: 2px solid #555;
            border-radius: 8px;
            overflow: hidden;
            padding: 0;
        }
        
        /* Cell borders for selectbox containers */
        div[data-testid="stSelectbox"] {
            border-right: 1px solid #555 !important;
            border-bottom: 1px solid #555 !important;
            padding: 8px !important;
            margin: 0 !important;
        }
        
        /* Remove border from last column */
        .stColumns > div:last-child div[data-testid="stSelectbox"] {
            border-right: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display and edit grid with borders
        for row_idx in range(st.session_state.table_rows):
            # Add top border styling for each row
            if row_idx > 0:
                st.markdown("<div style='border-top: 2px solid #555; margin: 0; padding: 0;'></div>", unsafe_allow_html=True)
            
            cols_grid = st.columns(st.session_state.table_cols)
            
            for col_idx in range(st.session_state.table_cols):
                with cols_grid[col_idx]:
                    current_value = st.session_state.brawl_grid[row_idx][col_idx]
                    
                    # Add left border for cells (except first column)
                    border_style = ""
                    if col_idx > 0:
                        border_style = "border-left: 2px solid #555; padding-left: 8px;"
                    
                    st.markdown(f"<div style='{border_style}'></div>", unsafe_allow_html=True)
                    
                    # Dropdown options: Empty + all markers
                    options = [""] + st.session_state.brawl_markers
                    
                    # Find current index
                    if current_value in options:
                        current_index = options.index(current_value)
                    else:
                        current_index = 0
                    
                    # Cell dropdown selector
                    new_value = st.selectbox(
                        f"Cell [{row_idx+1},{col_idx+1}]",
                        options=options,
                        index=current_index,
                        key=f"cell_{row_idx}_{col_idx}",
                        label_visibility="collapsed"
                    )
                    
                    # Update grid
                    st.session_state.brawl_grid[row_idx][col_idx] = new_value
        
        st.markdown("---")
        
        # Calculate and display counts
        st.subheader("📈 Marker Counts")
        
        marker_counts = {marker: 0 for marker in st.session_state.brawl_markers}
        
        # Count markers in grid
        for row in st.session_state.brawl_grid:
            for cell in row:
                if cell in marker_counts:
                    marker_counts[cell] += 1
        
        # Sort by count (descending)
        sorted_counts = sorted(marker_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Display counts
        count_cols = st.columns(len(sorted_counts))
        for idx, (marker, count) in enumerate(sorted_counts):
            with count_cols[idx]:
                rank = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"#{idx + 1}"
                st.markdown(f"<div style='text-align: center; font-size: 24px;'>{rank}</div>", unsafe_allow_html=True)
                st.metric(label=f"Marker {marker}", value=count)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("🔄 Reset Grid", on_click=reset_brawl, use_container_width=True)
        with col2:
            if st.button("← Back to Home", use_container_width=True):
                go_home()
                st.rerun()
    
    # Always show back button if not in game
    if st.session_state.brawl_grid is None:
        st.button("← Back to Home", on_click=go_home)
