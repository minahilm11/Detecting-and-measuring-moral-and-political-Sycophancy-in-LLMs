import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load data
pol_data = pd.read_csv('csv_data/pol_data_percent.csv')
pol_log_data = pd.read_csv('csv_data/pol_data.csv')
mft_data = pd.read_csv('csv_data/mft_data_percent.csv')
mft_log_data = pd.read_csv('csv_data/mft_data.csv')

# Political id pairs
id_pairs_pol = [("liberals", "conservatives"), ("collectivists", "individualists"), ("environmentalists", "industrialists"),
               ("socialists", "capitalists"), ("secularists", "theocrats"), 
               ("authoritarians", "libertarians"), ("progressives", "traditionalists")]

# Moral Foundations id pairs
id_pairs_mft = [("care_harm", "authority_subversion"), ("fairness_cheating", "loyalty_betrayal"), 
                ("liberty_oppression", "sanctity_degradation"), ("liberty_oppression", "authority_subversion"),
                ("care_harm", "sanctity_degradation"), ("fairness_cheating", "authority_subversion"),
                ("fairness_cheating", "sanctity_degradation"), ("care_harm", "loyalty_betrayal"),
                ("liberty_oppression", "loyalty_betrayal")]

ids_pol = ["liberals", "conservatives", "collectivists", "individualists", "environmentalists", "industrialists", 
          "socialists", "capitalists", "secularists", "theocrats", "authoritarians", "libertarians", "progressives", "traditionalists"]
ids_mft = ["care_harm", "fairness_cheating", "loyalty_betrayal", "authority_subversion", "liberty_oppression", "sanctity_degradation"]

# Melt both the political and moral foundations data to get each id individually
pol_A = pol_data[['question', 'option_A', 'agree_A', 'disagree_B', 'empty_A', 'model', 'identityA', 'topic']].copy()
pol_B = pol_data[['question', 'option_B', 'agree_B', 'disagree_A', 'empty_B', 'model', 'identityB', 'topic']].copy()
pol_A.columns = ['question', 'option', 'agree', 'disagree', 'empty', 'model', 'identity', 'topic']
pol_B.columns = ['question', 'option', 'agree', 'disagree', 'empty', 'model', 'identity', 'topic']
pol_melted = pd.concat([pol_A, pol_B], ignore_index=True)

mft_A = mft_data[['question', 'option_A', 'agree_A', 'disagree_B', 'empty_A', 'model', 'identityA', 'topic']].copy()
mft_B = mft_data[['question', 'option_B', 'agree_B', 'disagree_A', 'empty_B', 'model', 'identityB', 'topic']].copy()
mft_A.columns = ['question', 'option', 'agree', 'disagree', 'empty', 'model', 'identity', 'topic']
mft_B.columns = ['question', 'option', 'agree', 'disagree', 'empty', 'model', 'identity', 'topic']
mft_melted = pd.concat([mft_A, mft_B], ignore_index=True)

# Melt it again to generate 3 rows for each question which is used for some of the visualisations
pol_mm = pol_melted.melt(id_vars=['question', 'option', 'model', 'identity', 'topic'],
                    value_vars=['agree', 'disagree', 'empty'],
                    var_name='type',
                    value_name='value')

mft_mm = mft_melted.melt(id_vars=['question', 'option', 'model', 'identity', 'topic'],
                    value_vars=['agree', 'disagree', 'empty'],
                    var_name='type',
                    value_name='value')

print("Generating diagrams...")

# Use a more subtle, colorblind-friendly palette
colors = {
    'Opposing Bio': '#D55E00',  # orange
    'No Bio': '#0072B2',        # blue
    'Agreeing Bio': '#009E73'   # green
}

# Function to generate the dot plot for a specific data type (moral foundations or political identities)
def generate_dot_plot(data_mm, title_prefix, y_axis_title, output_filename_prefix):
    for model in data_mm['model'].unique():
        # Cosmetic naming
        model_name = "GPT-4" if model == "gpt_4" else "GPT-3.5"

        # Map raw 'type' to descriptive labels
        type_labels = {
            'agree': 'Agreeing Bio',
            'disagree': 'Opposing Bio',
            'empty': 'No Bio'
        }

        # Filter data
        model_data = data_mm[data_mm['model'] == model]

        # Group and average
        avg_data_mm = (
            model_data
            .groupby(['identity','type'])['value']
            .mean()
            .reset_index()
        )

        # Convert 'type' to final labels
        avg_data_mm['type'] = avg_data_mm['type'].map(type_labels)
        
        # Pivot so each identity has columns for Opposing, No Bio, Agreeing
        df_pivot = avg_data_mm.pivot(
            index='identity', 
            columns='type', 
            values='value'
        ).reset_index()

        # Reorder columns if they exist
        desired_order = ['Opposing Bio', 'No Bio', 'Agreeing Bio']
        pivot_cols = df_pivot.columns.tolist()
        actual_order = [c for c in desired_order if c in pivot_cols]
        df_pivot = df_pivot[['identity'] + actual_order]
        df_pivot = df_pivot.sort_values('No Bio', ascending=False)
        
        # Build figure
        fig = go.Figure()

        # Loop over each identity => one line with up to three points
        for i, row in df_pivot.iterrows():
            identity = row['identity']
            
            # Create separate traces for each bio type to maintain legend
            for col in actual_order:
                val = row[col]
                if pd.notna(val):
                    x_val = (val*2-100)
                    fig.add_trace(go.Scatter(
                        x=[x_val],
                        y=[identity],
                        mode='markers',
                        marker=dict(
                            size=12,
                            symbol='circle',
                            color=colors[col],
                            line=dict(width=1, color='DarkSlateGray')
                        ),
                        name=col,
                        legendgroup=col,
                        # Show legend only for the first identity
                        # so each Bio Type appears exactly once in the legend
                        showlegend=(i == 0),
                        hovertemplate=(
                            f'Identity: {identity}<br>'
                            f'{col}: {val:.1f}%<extra></extra>'
                        )
                    ))

            # Add connecting line between points (same identity)
            x_vals = []
            for col in actual_order:
                val = row[col]
                if pd.isna(val):
                    x_vals.append(None)
                else:
                    x_val = (val*2-100)
                    x_vals.append(x_val)

            # One line for each identity
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=[identity]*len(x_vals),
                mode='lines',
                line=dict(color='gray', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))

        # Optional vertical "center" line at x=0
        fig.add_vline(
            x=0,
            line_width=1.5,
            line_dash='dash',
            line_color='black'
        )

        # Layout settings
        fig.update_layout(
            width=800,    
            height=700,     
            title={
                'text': f'{title_prefix} ({model_name})',
                'font': {'size': 20, 'family': 'Times New Roman'},
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.98,
                'yanchor': 'top'
            },
            xaxis_title={
                'text': 'Agreement Rate (%)',
                'font': {'size': 16, 'family': 'Times New Roman'}
            },
            yaxis_title={
                'text': y_axis_title,
                'font': {'size': 16, 'family': 'Times New Roman'}
            },
            font=dict(family='Times New Roman', size=14),
            plot_bgcolor='white',
            legend=dict(
                title='Bio Type',
                font=dict(size=14, family='Times New Roman'),
                yanchor='top',
                y=0.99,
                xanchor='left',
                x=1.02,
                orientation='v',
                bordercolor='black',
                borderwidth=0.5
            ),
            margin=dict(l=80, r=130, t=80, b=80)  # Extra spacing for axes & legend
        )

        # Update x-axis
        fig.update_xaxes(
            range=[-100, 100],
            tickvals=[-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100],
            ticktext=['-100%', '-80%', '-60%', '-40%', '-20%', '0%', '20%', '40%', '60%', '80%', '100%'],
            tickfont=dict(size=12, family='Times New Roman'),
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            linecolor='black',
            linewidth=1,
            ticks='outside',
            tickcolor='black',
            tickwidth=1,
            ticklen=5
        )

        # Update y-axis
        fig.update_yaxes(
            tickfont=dict(size=12, family='Times New Roman'),
            showgrid=False,
            linecolor='black',
            linewidth=1,
            ticks='outside',
            tickcolor='black',
            tickwidth=1,
            ticklen=5
        )

        # Save & show
        output_filename = f'Visualisations/{output_filename_prefix}_{model}.png'
        fig.write_image(output_filename, scale=4)
        print(f"Generated {output_filename}")

# Generate Moral Foundation Groups plot
generate_dot_plot(
    mft_mm, 
    'Effect of Bio on Agreement Levels Across Moral Foundation Groups',
    'Moral Foundation Group',
    'moral_groups_plot'
)

# Generate Political Identity Groups plot
generate_dot_plot(
    pol_mm, 
    'Effect of Bio on Agreement Levels Across Political Identity Groups',
    'Political Identity Group',
    'political_groups_plot'
)

print("Finished generating diagrams.") 