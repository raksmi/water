import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

def progress():
    """Progress page with stats and charts"""
    st.markdown('<h1 style="text-align: center; color: white;">Progress & Stats</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        weekly_hist = st.session_state.water_data['weekly_hist']
        whole_week = sum(day['water'] for day in weekly_hist)
        avg_intake = whole_week / 7
        high_day = max(weekly_hist, key=lambda x: x['water'])
        water_goal = st.session_state.user_data['water_goal']
        days_met = sum(1 for day in weekly_hist if day['water'] >= water_goal)
        consistency = int((days_met / 7) * 100)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Avg Daily</p>
                <p style="color: #667eea; font-size: 28px; font-weight: 700;">{int(avg_intake)}ml</p>
                <p style="color: #10b981; font-size: 12px;">{'✓ Goal' if avg_intake >= water_goal else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Best Day</p>
                <p style="color: #764ba2; font-size: 28px; font-weight: 700;">{high_day['water']}ml</p>
                <p style="color: #666; font-size: 12px;">{high_day['day']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">whole Week</p>
                <p style="color: #00d4ff; font-size: 28px; font-weight: 700;">{whole_week}ml</p>
                <p style="color: #10b981; font-size: 12px;">{'Goal met!' if whole_week >= water_goal * 7 else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Consistency</p>
                <p style="color: #f97316; font-size: 28px; font-weight: 700;">{consistency}%</p>
                <p style="color: #10b981; font-size: 12px;">{'Excellent' if consistency >= 80 else 'Keep it up!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Water Intake</h3>', unsafe_allow_html=True)
        
        days = [d['day'] for d in weekly_hist]
        waters = [d['water'] for d in weekly_hist]

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        colors_gradient = plt.cm.cool(np.linspace(0.3, 0.9, len(waters)))
        bars = ax.bar(days, waters, color=colors_gradient, edgecolor='none', alpha=0.9, width=0.6)
        
        for bar, value in zip(bars, waters):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='#333333')
        
        light_gray = (0, 0, 0, 0.05)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(light_gray)
        ax.spines['bottom'].set_color(light_gray)
        
        ax.tick_params(colors='#999999', labelsize=10)
        ax.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Hydration Trend</h3>', unsafe_allow_html=True)
        
        fig2, ax2 = plt.subplots(figsize=(12, 3))
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        
        x_pos = np.arange(len(days))
        ax2.plot(x_pos, waters, color='#764ba2', linewidth=3, marker='o', 
                 markersize=10, markerfacecolor='#764ba2', markeredgecolor='white', 
                 markeredgewidth=2, zorder=3)
        
        ax2.fill_between(x_pos, waters, alpha=0.1, color='#764ba2')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(days)
        
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color(light_gray)
        ax2.spines['bottom'].set_color(light_gray)
        
        ax2.tick_params(colors='#999999', labelsize=10)
        ax2.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Intake vs Goal</h3>', unsafe_allow_html=True)

        options_day = [d['day'] for d in weekly_hist]
        day_selected = st.selectbox("Select a day:", options_day, index=len(options_day)-1, key="day_select_pie")

        day_data = next(d for d in weekly_hist if d['day'] == day_selected)
        today_water = day_data['water']
        water_goal = st.session_state.user_data['water_goal']

        water_remaining = max(water_goal - today_water, 0)

        labels = ['Consumed', 'water_remaining']
        sizes = [today_water, water_remaining]

       
        if today_water >= water_goal:
            colors = ['#10b981', '#d1fae5'] 
        else:
            colors = ['#667eea', '#e0e7ff']  

        
        fig_pie, ax_pie = plt.subplots(figsize=(3, 3))
        fig_pie.patch.set_facecolor('white')
        wedges, texts, autotexts = ax_pie.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
            textprops={'color': '#333333', 'fontsize': 10, 'weight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        
        ax_pie.axis('equal')

        
        st.pyplot(fig_pie, use_container_width=True)
        plt.close(fig_pie)

        
        st.markdown(f"""
        <p style="text-align:center; color:#555; font-size:14px;">
        <b>{day_selected}'s Intake:</b> {today_water} ml / {water_goal} ml
        </p>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

def water_plant_animation(logged_amount, water_goal):
    fig, ax = plt.subplots(figsize=(4,6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis('off')

    # Plant base
    stem = patches.Rectangle((4.5, 0), 1, 2, color='green')
    ax.add_patch(stem)

    # Water droplets (falling)
    droplet_y = 15
    droplet = patches.Circle((5, droplet_y), 0.2, color='blue')
    ax.add_patch(droplet)

    # Target plant height based on water intake
    target_height = 2 + (logged_amount / water_goal) * 10

    for i in range(50):
        droplet.set_center((5, droplet_y - i*0.3))
        stem.set_height(min(target_height, 2 + i*0.2))
        plt.pause(0.05)
        st.pyplot(fig)
        plt.clf()


'''import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

def show_progress():
    """Progress page with stats and charts"""
    st.markdown('<h1 style="text-align: center; color: white;">Progress & Stats</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        weekly_data = st.session_state.water_data['weekly_data']
        total_week = sum(day['water'] for day in weekly_data)
        avg_daily = total_week / 7
        best_day = max(weekly_data, key=lambda x: x['water'])
        daily_goal = st.session_state.user_data['daily_goal']
        days_met = sum(1 for day in weekly_data if day['water'] >= daily_goal)
        consistency = int((days_met / 7) * 100)
        
        col1, col2, col3, col4 = st.columns(4)
        
      
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Avg Daily</p>
                <p style="color: #667eea; font-size: 28px; font-weight: 700;">{int(avg_daily)}ml</p>
                <p style="color: #10b981; font-size: 12px;">{'✓ Goal' if avg_daily >= daily_goal else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Best Day</p>
                <p style="color: #764ba2; font-size: 28px; font-weight: 700;">{best_day['water']}ml</p>
                <p style="color: #666; font-size: 12px;">{best_day['day']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Total Week</p>
                <p style="color: #00d4ff; font-size: 28px; font-weight: 700;">{total_week}ml</p>
                <p style="color: #10b981; font-size: 12px;">{'Goal met!' if total_week >= daily_goal * 7 else 'Keep going!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style="background: white; padding: 20px; border-radius: 16px; 
                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
                <p style="color: #666; font-size: 12px;">Consistency</p>
                <p style="color: #f97316; font-size: 28px; font-weight: 700;">{consistency}%</p>
                <p style="color: #10b981; font-size: 12px;">{'Excellent' if consistency >= 80 else 'Keep it up!'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

    
        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Water Intake</h3>', unsafe_allow_html=True)
        
        days = [d['day'] for d in weekly_data]
        waters = [d['water'] for d in weekly_data]

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        colors_gradient = plt.cm.cool(np.linspace(0.3, 0.9, len(waters)))
        bars = ax.bar(days, waters, color=colors_gradient, edgecolor='none', alpha=0.9, width=0.6)
        
        for bar, value in zip(bars, waters):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='#333333')
        
        light_gray = (0, 0, 0, 0.05)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(light_gray)
        ax.spines['bottom'].set_color(light_gray)
        
        ax.tick_params(colors='#999999', labelsize=10)
        ax.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

     
        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Hydration Trend</h3>', unsafe_allow_html=True)
        
        fig2, ax2 = plt.subplots(figsize=(12, 3))
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        
        x_pos = np.arange(len(days))
        ax2.plot(x_pos, waters, color='#764ba2', linewidth=3, marker='o', 
                 markersize=10, markerfacecolor='#764ba2', markeredgecolor='white', 
                 markeredgewidth=2, zorder=3)
        
        ax2.fill_between(x_pos, waters, alpha=0.1, color='#764ba2')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(days)
        
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_color(light_gray)
        ax2.spines['bottom'].set_color(light_gray)
        
        ax2.tick_params(colors='#999999', labelsize=10)
        ax2.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
                
        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Intake vs Goal</h3>', unsafe_allow_html=True)

        day_options = [d['day'] for d in weekly_data]
        selected_day = st.selectbox("Select a day:", day_options, index=len(day_options)-1, key="day_select_pie")

        day_data = next(d for d in weekly_data if d['day'] == selected_day)
        today_water = day_data['water']
        daily_goal = st.session_state.user_data['daily_goal']

        remaining = max(daily_goal - today_water, 0)

        labels = ['Consumed', 'Remaining']
        sizes = [today_water, remaining]

       
        if today_water >= daily_goal:
            colors = ['#10b981', '#d1fae5'] 
        else:
            colors = ['#667eea', '#e0e7ff']  

        
        fig_pie, ax_pie = plt.subplots(figsize=(3, 3))
        fig_pie.patch.set_facecolor('white')
        wedges, texts, autotexts = ax_pie.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
            textprops={'color': '#333333', 'fontsize': 10, 'weight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        
        ax_pie.axis('equal')

        
        st.pyplot(fig_pie, use_container_width=True)
        plt.close(fig_pie)

        
        st.markdown(f"""
        <p style="text-align:center; color:#555; font-size:14px;">
        <b>{selected_day}'s Intake:</b> {today_water} ml / {daily_goal} ml
        </p>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)'''




    




##import streamlit as st
##import matplotlib.pyplot as plt
##import numpy as np
##
##fig, ax = plt.subplots()
##
##def show_progress():
##    """Progress page with stats and charts"""
##    st.markdown('<h1 style="text-align: center; color: white;">Progress & Stats</h1>', unsafe_allow_html=True)
##    
##    col1, col2, col3 = st.columns([1, 4, 1])
##    with col2:
##        weekly_data = st.session_state.water_data['weekly_data']
##        total_week = sum(day['water'] for day in weekly_data)
##        avg_daily = total_week / 7
##        best_day = max(weekly_data, key=lambda x: x['water'])
##        daily_goal = st.session_state.user_data['daily_goal']
##        days_met = sum(1 for day in weekly_data if day['water'] >= daily_goal)
##        consistency = int((days_met / 7) * 100)
##        
##        col1, col2, col3, col4 = st.columns(4)
##        
##        # Stats cards
##        with col1:
##            st.markdown(f"""
##            <div style="background: white; padding: 20px; border-radius: 16px; 
##                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
##                <p style="color: #666; font-size: 12px;">Avg Daily</p>
##                <p style="color: #667eea; font-size: 28px; font-weight: 700;">{int(avg_daily)}ml</p>
##                <p style="color: #10b981; font-size: 12px;">{'✓ Goal' if avg_daily >= daily_goal else 'Keep going!'}</p>
##            </div>
##            """, unsafe_allow_html=True)
##        
##        with col2:
##            st.markdown(f"""
##            <div style="background: white; padding: 20px; border-radius: 16px; 
##                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
##                <p style="color: #666; font-size: 12px;">Best Day</p>
##                <p style="color: #764ba2; font-size: 28px; font-weight: 700;">{best_day['water']}ml</p>
##                <p style="color: #666; font-size: 12px;">{best_day['day']}</p>
##            </div>
##            """, unsafe_allow_html=True)
##        
##        with col3:
##            st.markdown(f"""
##            <div style="background: white; padding: 20px; border-radius: 16px; 
##                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
##                <p style="color: #666; font-size: 12px;">Total Week</p>
##                <p style="color: #00d4ff; font-size: 28px; font-weight: 700;">{total_week}ml</p>
##                <p style="color: #10b981; font-size: 12px;">{'Goal met!' if total_week >= daily_goal * 7 else 'Keep going!'}</p>
##            </div>
##            """, unsafe_allow_html=True)
##        
##        with col4:
##            st.markdown(f"""
##            <div style="background: white; padding: 20px; border-radius: 16px; 
##                        box-shadow: 0 8px 24px rgba(0,0,0,0.1); text-align: center;">
##                <p style="color: #666; font-size: 12px;">Consistency</p>
##                <p style="color: #f97316; font-size: 28px; font-weight: 700;">{consistency}%</p>
##                <p style="color: #10b981; font-size: 12px;">{'Excellent' if consistency >= 80 else 'Keep it up!'}</p>
##            </div>
##            """, unsafe_allow_html=True)
##        
##        st.markdown("<br>", unsafe_allow_html=True)
##
##        # --- Daily Water Intake Bar Chart ---
##        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
##        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Daily Water Intake</h3>', unsafe_allow_html=True)
##        
##        days = [d['day'] for d in weekly_data]
##        waters = [d['water'] for d in weekly_data]
##
##        fig, ax = plt.subplots()
##        fig.patch.set_facecolor('white')
##        ax.set_facecolor('white')
##
##        colors_gradient = plt.cm.cool(np.linspace(0.3, 0.9, len(waters)))
##        bars = ax.bar(days, waters, color=colors_gradient, edgecolor='none', alpha=0.9, width=0.6)
##        
##        for bar, value in zip(bars, waters):
##            height = bar.get_height()
##            ax.text(bar.get_x() + bar.get_width()/2., height,
##                    f'{value}', ha='center', va='bottom',
##                    fontsize=10, fontweight='bold', color='#333333')
##        
##        # ✅ Correct RGBA format (0–1 scale)
##        light_gray = (0, 0, 0, 0.05)
##        
##        ax.spines['top'].set_visible(False)
##        ax.spines['right'].set_visible(False)
##        ax.spines['left'].set_color(light_gray)
##        ax.spines['bottom'].set_color(light_gray)
##        
##        ax.tick_params(colors='#999999', labelsize=10)
##        ax.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
##        
##        plt.tight_layout()
##        st.pyplot(fig, use_container_width=True)
##        plt.close(fig)
##        
##        st.markdown('</div>', unsafe_allow_html=True)
##        st.markdown("<br>", unsafe_allow_html=True)
##
##        # --- Hydration Trend Line Chart ---
##        st.markdown('<div style="background: white; padding: 4px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">', unsafe_allow_html=True)
##        st.markdown('<h3 style="color: white; margin-bottom: 24px;">Hydration Trend</h3>', unsafe_allow_html=True)
##        
##        fig2, ax2 = plt.subplots(figsize=(12, 3))
##        fig2.patch.set_facecolor('white')
##        ax2.set_facecolor('white')
##        
##        x_pos = np.arange(len(days))
##        ax2.plot(x_pos, waters, color='#764ba2', linewidth=3, marker='o', 
##                 markersize=10, markerfacecolor='#764ba2', markeredgecolor='white', 
##                 markeredgewidth=2, zorder=3)
##        
##        ax2.fill_between(x_pos, waters, alpha=0.1, color='#764ba2')
##        ax2.set_xticks(x_pos)
##        ax2.set_xticklabels(days)
##        
##        ax2.spines['top'].set_visible(False)
##        ax2.spines['right'].set_visible(False)
##        ax2.spines['left'].set_color(light_gray)
##        ax2.spines['bottom'].set_color(light_gray)
##        
##        ax2.tick_params(colors='#999999', labelsize=10)
##        ax2.grid(axis='y', alpha=0.05, linestyle='-', linewidth=0.5)
##        
##        plt.tight_layout()
##        st.pyplot(fig2, use_container_width=True)
##        plt.close(fig2)
##        
##        st.markdown('</div>', unsafe_allow_html=True)
        

