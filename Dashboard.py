# dashboard_defense_europeenne.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Analyse de la Défense Européenne - UE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #0055A4, #FFCC00, #009900);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0055A4;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #0055A4;
        border-bottom: 2px solid #0055A4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .pays-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #0055A4;
        background-color: #f8f9fa;
    }
    .euro-flag {
        background: linear-gradient(45deg, #0055A4, #FFCC00, #FFFFFF, #FF0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class DefenseEuropeenneDashboard:
    def __init__(self):
        self.pays_options = self.define_pays_options()
        self.composantes_options = self.define_composantes_options()
        
    def define_pays_options(self):
        """Définit les pays de l'UE disponibles pour l'analyse"""
        return [
            "Allemagne", "Autriche", "Belgique", "Bulgarie", "Chypre", "Croatie", "Danemark", "Espagne",
            "Estonie", "Finlande", "France", "Grece", "Hongrie", "Irlande", "Italie", "Lettonie", "Lituanie",
            "Luxembourg", "Malte", "Pays-Bas", "Pologne", "Portugal", "Republique Tcheque", "Roumanie",
            "Slovaquie", "Slovenie", "Suede", "UE-27"
        ]
    
    def define_composantes_options(self):
        """Définit les composantes militaires disponibles"""
        return [
            "Forces Terrestres", "Forces Maritimes", "Forces Aeriennes"
        ]
    
    def generate_defense_data(self, pays_composante):
        """Génère des données de défense simulées pour le dashboard"""
        # Période d'analyse : 2017-2027
        annees = list(range(2017, 2028))
        
        # Configuration de base selon le pays/composante
        config = self.get_config(pays_composante)
        
        data = {
            'Annee': annees,
            'Budget_Defense_Mds': self.simulate_budget(annees, config),
            'Personnel': self.simulate_personnel(annees, config),
            'Projets_PESCO': self.simulate_pesco_projects(annees, config),
            'Interoperabilite': self.simulate_interoperability(annees),
            'Capacite_Projection': self.simulate_projection_capacity(annees),
            'Temps_Reaction_Jours': self.simulate_reaction_time(annees),
            'Economies_Echelle_Mds': self.simulate_economies(annees, config),
            'Exercices_Communs': self.simulate_joint_exercises(annees),
            'Equipements_Interoperables': self.simulate_interoperable_equipment(annees)
        }
        
        # Ajouter des indicateurs spécifiques
        if config['type'] in ['pays_ue', 'union']:
            if 'cyberdefense' in config.get('specialisations', []):
                data['Capacite_Cyber'] = self.simulate_cyber_capacity(annees)
            if 'renseignement' in config.get('specialisations', []):
                data['Partage_Renseignement'] = self.simulate_intelligence_sharing(annees)
        
        return pd.DataFrame(data), config
    
    def get_config(self, pays_composante):
        """Retourne la configuration pour un pays/composante donné"""
        # Configuration simplifiée pour le dashboard
        configs = {
            "France": {
                "type": "pays_ue",
                "budget_base": 40.0,
                "personnel_base": 205000,
                "projets_pesco_base": 15,
                "specialisations": ["force_nucleaire", "intervention_rapide", "renseignement"]
            },
            "Allemagne": {
                "type": "pays_ue", 
                "budget_base": 45.0,
                "personnel_base": 180000,
                "projets_pesco_base": 18,
                "specialisations": ["blindes", "logistique", "cyberdefense"]
            },
            "UE-27": {
                "type": "union",
                "budget_base": 220.0,
                "personnel_base": 1450000,
                "projets_pesco_base": 60,
                "specialisations": ["defense_collective", "reaction_rapide", "cyberdefense"]
            },
            "Forces Terrestres": {
                "type": "composante",
                "personnel_base": 850000
            },
            "Forces Maritimes": {
                "type": "composante", 
                "personnel_base": 250000
            },
            "Forces Aeriennes": {
                "type": "composante",
                "personnel_base": 350000
            }
        }
        
        return configs.get(pays_composante, {
            "type": "pays_ue",
            "budget_base": 8.0,
            "personnel_base": 50000,
            "projets_pesco_base": 4,
            "specialisations": ["defense_generique"]
        })
    
    def simulate_budget(self, annees, config):
        """Simule l'évolution du budget défense"""
        budget_base = config.get('budget_base', 10.0)
        return [budget_base * (1 + 0.03 * (annee - 2017)) for annee in annees]
    
    def simulate_personnel(self, annees, config):
        """Simule l'évolution des effectifs"""
        personnel_base = config.get('personnel_base', 50000)
        return [personnel_base * (1 - 0.005 * (annee - 2017)) for annee in annees]
    
    def simulate_pesco_projects(self, annees, config):
        """Simule les projets PESCO"""
        base = config.get('projets_pesco_base', 5)
        projects = []
        for annee in annees:
            if annee < 2017:
                projects.append(0)
            elif annee < 2020:
                projects.append(base * (annee - 2016) // 3)
            elif annee < 2023:
                projects.append(base + 2 * (annee - 2019))
            else:
                projects.append(base + 6 + 3 * (annee - 2022))
        return projects
    
    def simulate_interoperability(self, annees):
        """Simule l'interopérabilité"""
        return [min(45 + 8 * (annee - 2017), 95) for annee in annees]
    
    def simulate_projection_capacity(self, annees):
        """Simule la capacité de projection"""
        return [min(30 + 7 * (annee - 2017), 95) for annee in annees]
    
    def simulate_reaction_time(self, annees):
        """Simule le temps de réaction"""
        return [max(30 - 2 * (annee - 2017), 7) for annee in annees]
    
    def simulate_economies(self, annees, config):
        """Simule les économies d'échelle"""
        base = 0.5 if config['type'] == 'pays_ue' else 2.0
        return [base * (annee - 2016) * 0.8 for annee in annees if annee >= 2017] + [0] * (2017 - min(annees))
    
    def simulate_joint_exercises(self, annees):
        """Simule les exercices communs"""
        return [10 + 3 * (annee - 2017) for annee in annees]
    
    def simulate_interoperable_equipment(self, annees):
        """Simule les équipements interopérables"""
        return [min(25 + 10 * (annee - 2017), 90) for annee in annees]
    
    def simulate_cyber_capacity(self, annees):
        """Simule la capacité cyber"""
        return [min(40 + 8 * (annee - 2017), 95) for annee in annees]
    
    def simulate_intelligence_sharing(self, annees):
        """Simule le partage de renseignement"""
        return [min(30 + 9 * (annee - 2017), 95) for annee in annees]
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">🛡️ Analyse de l\'Intégration Militaire Européenne</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="euro-flag">🇪🇺 DÉFENSE EUROPÉENNE UNIFIÉE 🇪🇺</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Analyse stratégique de l'intégration militaire européenne (2017-2027)**")
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Sélection du type d'analyse
        type_analyse = st.sidebar.radio(
            "Type d'analyse:",
            ["Pays de l'UE", "Composantes militaires", "UE-27 Global"]
        )
        
        if type_analyse == "Pays de l'UE":
            selection = st.sidebar.selectbox("Sélectionnez un pays:", self.pays_options[:-1])  # Exclure UE-27
        elif type_analyse == "Composantes militaires":
            selection = st.sidebar.selectbox("Sélectionnez une composante:", self.composantes_options)
        else:
            selection = "UE-27"
        
        # Options d'affichage
        st.sidebar.markdown("### 📊 Options de visualisation")
        show_projection = st.sidebar.checkbox("Afficher les projections 2023-2027", value=True)
        compare_before_after = st.sidebar.checkbox("Comparaison avant/après PESCO", value=True)
        
        return {
            'selection': selection,
            'type_analyse': type_analyse,
            'show_projection': show_projection,
            'compare_before_after': compare_before_after
        }
    
    def display_key_metrics(self, df, config):
        """Affiche les métriques clés"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS CLÉS DE PERFORMANCE</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques
        derniere_annee = df['Annee'].max()
        data_actuelle = df[df['Annee'] == derniere_annee].iloc[0]
        data_2017 = df[df['Annee'] == 2017].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'Budget_Defense_Mds' in df.columns:
                croissance_budget = ((data_actuelle['Budget_Defense_Mds'] - data_2017['Budget_Defense_Mds']) / 
                                   data_2017['Budget_Defense_Mds']) * 100
                st.metric(
                    "Budget Défense 2027",
                    f"{data_actuelle['Budget_Defense_Mds']:.1f} Md€",
                    f"{croissance_budget:+.1f}% vs 2017"
                )
        
        with col2:
            if 'Personnel' in df.columns:
                evolution_personnel = ((data_actuelle['Personnel'] - data_2017['Personnel']) / 
                                     data_2017['Personnel']) * 100
                st.metric(
                    "Effectifs 2027",
                    f"{data_actuelle['Personnel']:,.0f}",
                    f"{evolution_personnel:+.1f}% vs 2017"
                )
        
        with col3:
            croissance_interop = ((data_actuelle['Interoperabilite'] - data_2017['Interoperabilite']) / 
                                data_2017['Interoperabilite']) * 100
            st.metric(
                "Interopérabilité 2027",
                f"{data_actuelle['Interoperabilite']:.1f}%",
                f"{croissance_interop:+.1f}% vs 2017"
            )
        
        with col4:
            reduction_temps = ((data_2017['Temps_Reaction_Jours'] - data_actuelle['Temps_Reaction_Jours']) / 
                             data_2017['Temps_Reaction_Jours']) * 100
            st.metric(
                "Temps de Réaction 2027",
                f"{data_actuelle['Temps_Reaction_Jours']:.1f} jours",
                f"{reduction_temps:+.1f}% vs 2017"
            )
    
    def create_budget_analysis(self, df, config):
        """Analyse des budgets et effectifs"""
        st.markdown('<h3 class="section-header">💰 ANALYSE BUDGÉTAIRE ET EFFECTIFS</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Budget_Defense_Mds' in df.columns:
                fig = px.line(df, x='Annee', y='Budget_Defense_Mds',
                             title="Évolution du Budget de Défense (2017-2027)",
                             labels={'Budget_Defense_Mds': 'Budget (Md€)', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#0055A4', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Personnel' in df.columns:
                fig = px.line(df, x='Annee', y='Personnel',
                             title="Évolution des Effectifs (2017-2027)",
                             labels={'Personnel': 'Effectifs', 'Annee': 'Année'})
                fig.update_traces(line=dict(color='#FF0000', width=3))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_cooperation_analysis(self, df, config):
        """Analyse de la coopération européenne"""
        st.markdown('<h3 class="section-header">🤝 COOPÉRATION EUROPÉENNE</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='Annee', y='Projets_PESCO',
                         title="Projets PESCO (2017-2027)",
                         labels={'Projets_PESCO': 'Nombre de projets', 'Annee': 'Année'})
            fig.update_traces(line=dict(color='#0055A4', width=3))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(df, x='Annee', y='Exercices_Communs',
                         title="Exercices Militaires Communs (2017-2027)",
                         labels={'Exercices_Communs': "Nombre d'exercices", 'Annee': 'Année'})
            fig.update_traces(line=dict(color='#009900', width=3))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_capabilities_analysis(self, df, config):
        """Analyse des capacités opérationnelles"""
        st.markdown('<h3 class="section-header">⚡ CAPACITÉS OPÉRATIONNELLES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Graphique combiné des capacités
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(x=df['Annee'], y=df['Interoperabilite'],
                                    mode='lines', name='Interopérabilité',
                                    line=dict(color='#0055A4', width=3)))
            
            fig.add_trace(go.Scatter(x=df['Annee'], y=df['Capacite_Projection'],
                                    mode='lines', name='Capacité de Projection',
                                    line=dict(color='#FF0000', width=3)))
            
            if 'Equipements_Interoperables' in df.columns:
                fig.add_trace(go.Scatter(x=df['Annee'], y=df['Equipements_Interoperables'],
                                        mode='lines', name='Équipements Interopérables',
                                        line=dict(color='#009900', width=3)))
            
            fig.update_layout(title="Évolution des Capacités Opérationnelles (2017-2027)",
                             xaxis_title="Année",
                             yaxis_title="Niveau (%)",
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Temps de réaction
            fig = px.line(df, x='Annee', y='Temps_Reaction_Jours',
                         title="Temps de Réaction Opérationnel (2017-2027)",
                         labels={'Temps_Reaction_Jours': 'Jours', 'Annee': 'Année'})
            fig.update_traces(line=dict(color='#FF6600', width=3))
            fig.update_layout(height=500)
            fig.update_yaxes(autorange="reversed")  # Moins de jours = mieux
            st.plotly_chart(fig, use_container_width=True)
    
    def create_efficiency_analysis(self, df, config):
        """Analyse de l'efficacité et des économies"""
        st.markdown('<h3 class="section-header">📈 EFFICACITÉ ET ÉCONOMIES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='Annee', y='Economies_Echelle_Mds',
                         title="Économies d'Échelle Réalisées (2017-2027)",
                         labels={'Economies_Echelle_Mds': 'Économies (Md€)', 'Annee': 'Année'})
            fig.update_traces(line=dict(color='#009900', width=3))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Graphique des spécialisations
            special_data = []
            for col in ['Capacite_Cyber', 'Partage_Renseignement']:
                if col in df.columns:
                    special_data.append(col)
            
            if special_data:
                fig = go.Figure()
                colors = ['#0055A4', '#FF0000', '#FFCC00']
                
                for i, col in enumerate(special_data):
                    nom = col.replace('_', ' ').title()
                    fig.add_trace(go.Scatter(x=df['Annee'], y=df[col],
                                            mode='lines', name=nom,
                                            line=dict(color=colors[i % len(colors)], width=3)))
                
                fig.update_layout(title="Capacités Spécialisées (2017-2027)",
                                 xaxis_title="Année",
                                 yaxis_title="Niveau (%)",
                                 height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def create_comparative_analysis(self, df, config):
        """Analyse comparative avant/après intégration"""
        st.markdown('<h3 class="section-header">📊 ANALYSE COMPARATIVE</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des moyennes avant et après 2017 (lancement PESCO)
        avant_2017 = df[df['Annee'] < 2017]
        apres_2017 = df[df['Annee'] >= 2017]
        
        if len(avant_2017) > 0 and len(apres_2017) > 0:
            indicateurs = ['Interoperabilite', 'Capacite_Projection', 'Projets_PESCO']
            noms = ['Interopérabilité', 'Capacité Projection', 'Projets PESCO']
            
            valeurs_avant = [avant_2017[ind].mean() for ind in indicateurs]
            valeurs_apres = [apres_2017[ind].mean() for ind in indicateurs]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(name='Avant 2017', x=noms, y=valeurs_avant,
                                marker_color='#0055A4'))
            fig.add_trace(go.Bar(name='Après 2017', x=noms, y=valeurs_apres,
                                marker_color='#FF0000'))
            
            fig.update_layout(title="Comparaison Avant/Après Lancement de PESCO",
                             barmode='group',
                             height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    def create_strategic_insights(self, df, config, selection):
        """Génère des insights stratégiques"""
        st.markdown('<h3 class="section-header">💡 INSIGHTS STRATÉGIQUES</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des indicateurs de performance
        croissance_interop = ((df['Interoperabilite'].iloc[-1] - df['Interoperabilite'].iloc[0]) / 
                            df['Interoperabilite'].iloc[0]) * 100
        
        reduction_temps = ((df['Temps_Reaction_Jours'].iloc[0] - df['Temps_Reaction_Jours'].iloc[-1]) / 
                         df['Temps_Reaction_Jours'].iloc[0]) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 PERFORMANCES CLÉS")
            st.markdown(f"""
            - **Interopérabilité**: +{croissance_interop:.1f}% depuis 2017
            - **Temps de réaction**: -{reduction_temps:.1f}% depuis 2017  
            - **Projets PESCO**: {df['Projets_PESCO'].iloc[-1]:.0f} projets actifs
            - **Exercices communs**: {df['Exercices_Communs'].iloc[-1]:.0f} par an
            """)
            
            if 'Economies_Echelle_Mds' in df.columns:
                economies_totales = df['Economies_Echelle_Mds'].sum()
                st.markdown(f"- **Économies réalisées**: {economies_totales:.1f} Md€")
        
        with col2:
            st.markdown("#### 🚀 RECOMMANDATIONS")
            
            if config['type'] == 'pays_ue':
                st.markdown("""
                - Poursuivre l'harmonisation des équipements
                - Développer les capacités de projection
                - Renforcer la coopération cyberdéfense
                - Augmenter les exercices multinationaux
                """)
            elif config['type'] == 'union':
                st.markdown("""
                - Accélérer les projets PESCO
                - Standardiser les procédures opérationnelles
                - Développer des capacités stratégiques communes
                - Renforcer le commandement intégré
                """)
            elif config['type'] == 'composante':
                st.markdown("""
                - Standardiser les équipements et formations
                - Développer des centres d'excellence
                - Créer des brigades multinationales
                - Renforcer l'interopérabilité technique
                """)
        
        # Analyse des spécialisations
        if config['type'] in ['pays_ue', 'union']:
            st.markdown("#### 🌟 SPÉCIALISATIONS")
            specialisations = config.get('specialisations', [])
            if specialisations:
                for spec in specialisations:
                    st.markdown(f"- {spec.replace('_', ' ').title()}")
    
    def create_european_overview(self):
        """Vue d'ensemble européenne"""
        st.markdown('<h3 class="section-header">🌍 VUE D\'ENSEMBLE EUROPÉENNE</h3>', 
                   unsafe_allow_html=True)
        
        # Données comparatives des principaux pays
        pays_principaux = ["France", "Allemagne", "Italie", "Espagne", "Pologne", "UE-27"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 💰 BUDGETS DÉFENSE 2027")
            budgets = {
                "France": 52.3, "Allemagne": 58.5, "Italie": 32.5, 
                "Espagne": 23.4, "Pologne": 15.6, "UE-27": 285.0
            }
            for pays, budget in budgets.items():
                st.progress(budget/max(budgets.values()), text=f"{pays}: {budget} Md€")
        
        with col2:
            st.markdown("#### 👥 EFFECTIFS MILITAIRES")
            effectifs = {
                "France": 205000, "Allemagne": 180000, "Italie": 165000,
                "Espagne": 124000, "Pologne": 115000, "UE-27": 1420000
            }
            for pays, eff in effectifs.items():
                st.progress(eff/max(effectifs.values()), text=f"{pays}: {eff:,}")
        
        with col3:
            st.markdown("#### 🤝 PROJETS PESCO")
            projets = {
                "France": 15, "Allemagne": 18, "Italie": 12,
                "Espagne": 10, "Pologne": 8, "UE-27": 60
            }
            for pays, proj in projets.items():
                st.progress(proj/max(projets.values()), text=f"{pays}: {proj} projets")

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Génération des données
        df, config = self.generate_defense_data(controls['selection'])
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Vue d'Ensemble", 
            "💰 Budgets & Effectifs", 
            "🤝 Coopération", 
            "⚡ Capacités", 
            "📈 Efficacité",
            "🌍 Europe"
        ])
        
        with tab1:
            st.markdown(f"## 🛡️ Analyse de la Défense - {controls['selection']}")
            self.display_key_metrics(df, config)
            self.create_strategic_insights(df, config, controls['selection'])
        
        with tab2:
            self.create_budget_analysis(df, config)
        
        with tab3:
            self.create_cooperation_analysis(df, config)
        
        with tab4:
            self.create_capabilities_analysis(df, config)
        
        with tab5:
            self.create_efficiency_analysis(df, config)
            if controls['compare_before_after']:
                self.create_comparative_analysis(df, config)
        
        with tab6:
            self.create_european_overview()
            
            st.markdown("---")
            st.markdown("""
            #### 📋 À PROPOS DE CE DASHBOARD
            
            Ce dashboard présente une analyse stratégique de l'intégration militaire européenne 
            depuis le lancement de la Coopération Structurée Permanente (PESCO) en 2017.
            
            **Période d'analyse**: 2017-2027  
            **Indicateurs suivis**: 
            - Budgets de défense et effectifs
            - Projets PESCO et coopération
            - Interopérabilité et capacités
            - Efficacité opérationnelle
            - Économies d'échelle
            
            **Objectif**: Mesurer les progrès de l'intégration militaire européenne et identifier 
            les domaines d'amélioration pour une défense européenne plus unie et efficace.
            """)

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = DefenseEuropeenneDashboard()
    dashboard.run_dashboard()