import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Analyse Avancee de Donnees CSV')

# Upload du fichier
uploaded_file = st.file_uploader("Choisir un fichier CSV")

if uploaded_file is not None:
    # Lecture du fichier
    df = pd.read_csv(uploaded_file)
    
    # Convertir tous les types pour eviter les erreurs Arrow
    df = df.astype(str)
    
    # Sidebar avec filtres
    st.sidebar.header('Filtres')
    
    # Detecter les colonnes numeriques potentielles
    numeric_cols = []
    for col in df.columns:
        try:
            df[col + '_numeric'] = pd.to_numeric(df[col], errors='coerce')
            if df[col + '_numeric'].notna().sum() > len(df) * 0.5:
                numeric_cols.append(col)
        except:
            pass
    
    # Si on detecte une colonne d'annee
    year_col = None
    for col in df.columns:
        if 'year' in col.lower() or 'date' in col.lower():
            try:
                df[col + '_year'] = pd.to_numeric(df[col], errors='coerce')
                if df[col + '_year'].notna().sum() > 0:
                    year_col = col
                    break
            except:
                pass
    
    # Filtre par annee si disponible
    if year_col:
        df[year_col + '_clean'] = pd.to_numeric(df[year_col], errors='coerce')
        df_year_filtered = df[df[year_col + '_clean'].notna()].copy()
        
        if len(df_year_filtered) > 0:
            min_year = int(df_year_filtered[year_col + '_clean'].min())
            max_year = int(df_year_filtered[year_col + '_clean'].max())
            
            year_range = st.sidebar.slider(
                'Selectionner la plage d\'annees',
                min_year,
                max_year,
                (min_year, max_year)
            )
            
            df_filtered = df_year_filtered[
                (df_year_filtered[year_col + '_clean'] >= year_range[0]) & 
                (df_year_filtered[year_col + '_clean'] <= year_range[1])
            ]
        else:
            df_filtered = df.copy()
    else:
        df_filtered = df.copy()
    
    # Detecter colonne type/categorie
    cat_col = None
    for col in df.columns:
        if 'type' in col.lower() or 'category' in col.lower() or 'genre' in col.lower():
            if df[col].nunique() < 20:  # Pas trop de categories
                cat_col = col
                break
    
    # Si pas trouve, prendre la premiere colonne avec peu de valeurs uniques
    if not cat_col:
        for col in df.columns:
            if df[col].nunique() < 20 and df[col].nunique() > 1:
                cat_col = col
                break
    
    # Filtre par categorie
    if cat_col:
        categories = ['Tous'] + list(df[cat_col].unique())
        selected_cat = st.sidebar.selectbox(f'Filtrer par {cat_col}', categories)
        
        if selected_cat != 'Tous':
            df_filtered = df_filtered[df_filtered[cat_col] == selected_cat]
    
    # Afficher le nombre de resultats
    st.sidebar.write(f'Nombre de resultats: {len(df_filtered)}')
    
    # Creation des onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        'Apercu',
        'Distribution',
        'Analyse Temporelle',
        'Analyse Detaillee'
    ])
    
    # ========== ONGLET 1: APERCU ==========
    with tab1:
        st.header('Apercu du dataset')
        
        col1, col2, col3 = st.columns(3)
        col1.metric('Nombre total', len(df_filtered))
        col2.metric('Colonnes', len(df_filtered.columns))
        col3.metric('Valeurs manquantes', df_filtered.isnull().sum().sum())
        
        st.subheader('Premieres lignes')
        # Convertir en string pour eviter les erreurs Arrow
        st.dataframe(df_filtered.head(10).astype(str))
        
        st.subheader('Types de donnees')
        type_df = pd.DataFrame({
            'Colonne': df_filtered.columns,
            'Type': df_filtered.dtypes.astype(str)
        })
        st.dataframe(type_df)
    
    # ========== ONGLET 2: DISTRIBUTION ==========
    with tab2:
        st.header('Distribution des contenus')
        
        if cat_col:
            # Compter les categories
            cat_counts = df_filtered[cat_col].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader('Diagramme en camembert')
                
                # Creer le pie chart avec matplotlib
                fig, ax = plt.subplots(figsize=(8, 6))
                
                # Gerer l'explode dynamiquement
                explode = [0.05] + [0] * (len(cat_counts) - 1)
                
                ax.pie(
                    cat_counts.values,
                    labels=cat_counts.index,
                    autopct='%1.1f%%',
                    explode=explode,
                    shadow=True,
                    startangle=90
                )
                ax.axis('equal')
                st.pyplot(fig)
            
            with col2:
                st.subheader('Graphique en barres')
                st.bar_chart(cat_counts)
                
                st.subheader('Details')
                for category in cat_counts.index:
                    count = cat_counts[category]
                    percentage = (count / len(df_filtered)) * 100
                    st.write(f'{category}: {count} ({percentage:.1f}%)')
        else:
            st.warning('Aucune colonne categorielle detectee')
        
        # Distribution par d'autres colonnes
        st.subheader('Distribution par colonne')
        col_to_analyze = st.selectbox('Choisir une colonne', df_filtered.columns)
        
        if col_to_analyze:
            value_counts = df_filtered[col_to_analyze].value_counts().head(10)
            st.bar_chart(value_counts)
    
    # ========== ONGLET 3: ANALYSE TEMPORELLE ==========
    with tab3:
        st.header('Analyse temporelle')
        
        if year_col:
            st.subheader('Evolution par annee')
            
            # Convertir en numerique
            df_filtered[year_col + '_num'] = pd.to_numeric(df_filtered[year_col], errors='coerce')
            df_year = df_filtered[df_filtered[year_col + '_num'].notna()].copy()
            
            if len(df_year) > 0:
                yearly_counts = df_year[year_col + '_num'].value_counts().sort_index()
                st.line_chart(yearly_counts)
                
                # Top 5 des annees
                st.subheader('Top 5 des annees les plus representatives')
                top_years = yearly_counts.nlargest(5)
                st.bar_chart(top_years)
                
                # Stats
                col1, col2, col3 = st.columns(3)
                col1.metric('Annee min', int(df_year[year_col + '_num'].min()))
                col2.metric('Annee max', int(df_year[year_col + '_num'].max()))
                col3.metric('Annee mediane', int(df_year[year_col + '_num'].median()))
            else:
                st.warning('Pas de donnees temporelles valides')
        else:
            st.warning('Aucune colonne de date ou annee detectee')
    
    # ========== ONGLET 4: ANALYSE DETAILLEE ==========
    with tab4:
        st.header('Analyse detaillee')
        
        # Trouver colonne geographique
        geo_col = None
        for col in df.columns:
            if 'country' in col.lower() or 'pays' in col.lower() or 'location' in col.lower():
                geo_col = col
                break
        
        if geo_col:
            st.subheader(f'Analyse par {geo_col}')
            
            # Extraire tous les pays (gerer les virgules)
            countries_list = []
            for countries in df_filtered[geo_col].dropna():
                if ',' in str(countries):
                    countries_split = [c.strip() for c in str(countries).split(',')]
                    countries_list.extend(countries_split)
                else:
                    countries_list.append(str(countries))
            
            if len(countries_list) > 0:
                # Compter les pays
                countries_series = pd.Series(countries_list)
                
                # Slider pour le nombre
                top_n = st.slider('Nombre de resultats a afficher', 5, 20, 10)
                top_countries = countries_series.value_counts().head(top_n)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f'Top {top_n}')
                    st.bar_chart(top_countries)
                
                with col2:
                    st.subheader('Camembert (Top 5)')
                    
                    top_5 = countries_series.value_counts().head(5)
                    
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.pie(
                        top_5.values,
                        labels=top_5.index,
                        autopct='%1.1f%%',
                        startangle=90
                    )
                    ax.axis('equal')
                    st.pyplot(fig)
            else:
                st.warning('Pas de donnees geographiques')
        else:
            st.info('Analyse des colonnes disponibles')
            
            # Afficher statistiques sur toutes les colonnes
            for col in df_filtered.columns[:5]:  # Limiter a 5 colonnes
                st.subheader(f'Colonne: {col}')
                st.write(f'Valeurs uniques: {df_filtered[col].nunique()}')
                st.write(f'Valeurs manquantes: {df_filtered[col].isnull().sum()}')
                
                if df_filtered[col].nunique() < 20:
                    value_counts = df_filtered[col].value_counts().head(10)
                    st.bar_chart(value_counts)
    
    # Section de recherche
    st.header('Recherche dans le dataset')
    
    # Choisir colonne de recherche
    search_col = st.selectbox('Colonne de recherche', df_filtered.columns)
    search_term = st.text_input('Terme a rechercher')
    
    if search_term and search_col:
        search_results = df_filtered[
            df_filtered[search_col].astype(str).str.contains(search_term, case=False, na=False)
        ]
        st.write(f'Resultats trouves: {len(search_results)}')
        if len(search_results) > 0:
            st.dataframe(search_results.head(20).astype(str))
        else:
            st.info('Aucun resultat trouve')

else:
    st.info('Veuillez charger un fichier CSV pour commencer l\'analyse')
    
    st.write('Cette application permet de:')
    st.write('- Analyser n\'importe quel fichier CSV')
    st.write('- Filtrer les donnees automatiquement')
    st.write('- Visualiser avec des diagrammes en camembert')
    st.write('- Analyser l\'evolution temporelle si disponible')
    st.write('- Explorer les donnees avec des filtres interactifs')