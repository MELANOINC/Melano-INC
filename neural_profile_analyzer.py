#!/usr/bin/env python3
"""
MELANO INC - NEURAL PROFILE ANALYZER
Advanced AI-powered profile analysis system with deep learning capabilities
CLASSIFIED - NEURAL INTELLIGENCE FOR LEAD QUALIFICATION
"""

import asyncio
import json
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
import logging
import re
import hashlib
from pathlib import Path

# Neural network imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    import torch
    import torch.nn as nn
    import torch.optim as optim
    DEEP_LEARNING_AVAILABLE = True
except ImportError:
    DEEP_LEARNING_AVAILABLE = False
    print("⚠️ Deep Learning frameworks no disponibles - usando análisis básico")

# ML imports
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ Scikit-learn no disponible - funcionalidad limitada")

# NLP imports
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("⚠️ NLTK no disponible - análisis de texto limitado")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("⚠️ SpaCy no disponible - análisis de entidades limitado")

@dataclass
class NeuralProfileAnalysis:
    """Análisis neural completo de perfil"""
    profile_id: str
    analysis_timestamp: datetime
    
    # Scores neurales principales
    lead_quality_score: float  # 0-1
    investment_propensity_score: float  # 0-1
    engagement_likelihood_score: float  # 0-1
    conversion_probability_score: float  # 0-1
    
    # Análisis de personalidad neural
    personality_traits: Dict[str, float]  # Big Five + custom traits
    communication_style: Dict[str, float]
    decision_making_style: str
    risk_tolerance: float
    
    # Análisis de contenido neural
    content_sentiment_analysis: Dict[str, Any]
    topic_modeling_results: Dict[str, Any]
    expertise_areas: List[Dict[str, float]]
    influence_indicators: Dict[str, float]
    
    # Análisis de comportamiento neural
    activity_patterns: Dict[str, Any]
    engagement_patterns: Dict[str, Any]
    network_analysis: Dict[str, Any]
    temporal_behavior: Dict[str, Any]
    
    # Predicciones neurales
    response_time_prediction: float  # horas
    optimal_contact_time: str
    preferred_communication_channel: str
    message_tone_preference: str
    
    # Segmentación neural
    neural_segment: str
    segment_confidence: float
    similar_profiles: List[str]
    
    # Métricas de confianza
    analysis_confidence: float
    model_version: str
    feature_importance: Dict[str, float]

@dataclass
class NeuralLeadScore:
    """Score neural de lead con explicabilidad"""
    profile_id: str
    overall_score: float
    component_scores: Dict[str, float]
    confidence_interval: Tuple[float, float]
    score_explanation: List[str]
    risk_factors: List[str]
    opportunity_factors: List[str]
    recommended_actions: List[str]
    score_timestamp: datetime

class NeuralProfileAnalyzer:
    """Analizador neural avanzado de perfiles"""
    
    def __init__(self, config_path: str = "neural_analyzer_config.json"):
        self.config = self.load_config(config_path)
        self.logger = self.setup_logger()
        self.db_path = "neural_analysis.db"
        
        # Modelos neurales
        self.deep_learning_models = {}
        self.ml_models = {}
        self.nlp_models = {}
        
        # Vectorizadores y escaladores
        self.text_vectorizers = {}
        self.feature_scalers = {}
        self.label_encoders = {}
        
        # Cache de análisis
        self.analysis_cache = {}
        self.model_cache = {}
        
        # Métricas de rendimiento
        self.performance_metrics = {}
        self.prediction_accuracy = {}
        
        self.init_database()
        asyncio.create_task(self.initialize_neural_models())
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Carga configuración del analizador neural"""
        default_config = {
            "neural_analyzer": {
                "deep_learning": {
                    "enabled": True,
                    "model_architecture": "transformer",
                    "hidden_layers": [512, 256, 128, 64],
                    "dropout_rate": 0.3,
                    "learning_rate": 0.001,
                    "batch_size": 32,
                    "epochs": 100,
                    "early_stopping_patience": 10
                },
                
                "feature_engineering": {
                    "text_features": {
                        "max_features": 10000,
                        "ngram_range": [1, 3],
                        "min_df": 2,
                        "max_df": 0.95,
                        "use_tfidf": True,
                        "use_word2vec": True,
                        "use_bert_embeddings": True
                    },
                    "behavioral_features": {
                        "activity_window_days": 90,
                        "engagement_metrics": True,
                        "temporal_patterns": True,
                        "network_features": True
                    },
                    "demographic_features": {
                        "industry_encoding": "target",
                        "location_encoding": "frequency",
                        "company_size_encoding": "ordinal",
                        "seniority_encoding": "ordinal"
                    }
                },
                
                "model_ensemble": {
                    "use_ensemble": True,
                    "models": [
                        "neural_network",
                        "gradient_boosting",
                        "random_forest",
                        "svm",
                        "logistic_regression"
                    ],
                    "ensemble_method": "weighted_voting",
                    "cross_validation_folds": 5
                },
                
                "personality_analysis": {
                    "big_five_model": True,
                    "custom_traits": [
                        "tech_savviness",
                        "investment_orientation",
                        "risk_appetite",
                        "innovation_adoption",
                        "relationship_building"
                    ],
                    "sentiment_analysis": True,
                    "emotion_detection": True
                },
                
                "lead_scoring": {
                    "scoring_factors": {
                        "demographic_fit": 0.25,
                        "behavioral_indicators": 0.30,
                        "content_analysis": 0.20,
                        "engagement_history": 0.15,
                        "network_influence": 0.10
                    },
                    "threshold_high_quality": 0.75,
                    "threshold_medium_quality": 0.50,
                    "threshold_low_quality": 0.25
                },
                
                "prediction_models": {
                    "response_time_model": "lstm",
                    "conversion_model": "transformer",
                    "churn_model": "gradient_boosting",
                    "lifetime_value_model": "neural_network"
                },
                
                "explainability": {
                    "use_shap": True,
                    "use_lime": True,
                    "feature_importance": True,
                    "decision_trees": True,
                    "counterfactual_explanations": True
                }
            }
        }
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except FileNotFoundError:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        return default_config
    
    def setup_logger(self) -> logging.Logger:
        """Configura logging para el analizador neural"""
        logger = logging.getLogger('NeuralProfileAnalyzer')
        logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler('neural_analyzer.log')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [NEURAL ANALYZER] - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_formatter = logging.Formatter('🧠 NEURAL ANALYZER - %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def init_database(self):
        """Inicializa base de datos del analizador neural"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de análisis neurales
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS neural_analyses (
                    profile_id TEXT PRIMARY KEY,
                    analysis_timestamp TIMESTAMP,
                    lead_quality_score REAL,
                    investment_propensity_score REAL,
                    engagement_likelihood_score REAL,
                    conversion_probability_score REAL,
                    personality_traits TEXT,
                    communication_style TEXT,
                    decision_making_style TEXT,
                    risk_tolerance REAL,
                    content_sentiment_analysis TEXT,
                    topic_modeling_results TEXT,
                    expertise_areas TEXT,
                    influence_indicators TEXT,
                    activity_patterns TEXT,
                    engagement_patterns TEXT,
                    network_analysis TEXT,
                    temporal_behavior TEXT,
                    response_time_prediction REAL,
                    optimal_contact_time TEXT,
                    preferred_communication_channel TEXT,
                    message_tone_preference TEXT,
                    neural_segment TEXT,
                    segment_confidence REAL,
                    similar_profiles TEXT,
                    analysis_confidence REAL,
                    model_version TEXT,
                    feature_importance TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de scores de leads
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS neural_lead_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT,
                    overall_score REAL,
                    component_scores TEXT,
                    confidence_interval TEXT,
                    score_explanation TEXT,
                    risk_factors TEXT,
                    opportunity_factors TEXT,
                    recommended_actions TEXT,
                    score_timestamp TIMESTAMP,
                    model_version TEXT,
                    FOREIGN KEY (profile_id) REFERENCES neural_analyses (profile_id)
                )
            ''')
            
            # Tabla de entrenamiento de modelos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_training_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT,
                    features TEXT,
                    labels TEXT,
                    data_source TEXT,
                    quality_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de métricas de modelos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS model_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_name TEXT,
                    model_version TEXT,
                    metric_name TEXT,
                    metric_value REAL,
                    evaluation_date TIMESTAMP,
                    dataset_size INTEGER,
                    cross_validation_score REAL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("Base de datos Neural Analyzer inicializada")
            
        except Exception as e:
            self.logger.error(f"Error inicializando base de datos: {str(e)}")
    
    async def initialize_neural_models(self):
        """Inicializa modelos neurales y de ML"""
        try:
            self.logger.info("🧠 Inicializando modelos neurales...")
            
            # Inicializar modelos de deep learning
            if DEEP_LEARNING_AVAILABLE:
                await self.init_deep_learning_models()
            
            # Inicializar modelos de ML tradicional
            if SKLEARN_AVAILABLE:
                await self.init_ml_models()
            
            # Inicializar modelos de NLP
            await self.init_nlp_models()
            
            # Inicializar vectorizadores
            await self.init_vectorizers()
            
            self.logger.info("✅ Modelos neurales inicializados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error inicializando modelos neurales: {str(e)}")
    
    async def init_deep_learning_models(self):
        """Inicializa modelos de deep learning"""
        try:
            config = self.config["neural_analyzer"]["deep_learning"]
            
            # Modelo principal de análisis de perfiles
            self.deep_learning_models["profile_analyzer"] = self.create_profile_analyzer_model(
                input_dim=1000,  # Ajustar según features
                hidden_layers=config["hidden_layers"],
                dropout_rate=config["dropout_rate"]
            )
            
            # Modelo de predicción de conversión
            self.deep_learning_models["conversion_predictor"] = self.create_conversion_model()
            
            # Modelo de análisis de sentimientos
            self.deep_learning_models["sentiment_analyzer"] = self.create_sentiment_model()
            
            # Modelo de segmentación
            self.deep_learning_models["segmentation_model"] = self.create_segmentation_model()
            
            self.logger.info("Modelos de deep learning inicializados")
            
        except Exception as e:
            self.logger.error(f"Error inicializando deep learning: {str(e)}")
    
    def create_profile_analyzer_model(self, input_dim: int, hidden_layers: List[int], dropout_rate: float):
        """Crea modelo neural principal para análisis de perfiles"""
        if not DEEP_LEARNING_AVAILABLE:
            return None
        
        model = keras.Sequential([
            layers.Input(shape=(input_dim,)),
            layers.BatchNormalization(),
        ])
        
        # Capas ocultas
        for i, units in enumerate(hidden_layers):
            model.add(layers.Dense(units, activation='relu', name=f'hidden_{i+1}'))
            model.add(layers.Dropout(dropout_rate))
            model.add(layers.BatchNormalization())
        
        # Capas de salida múltiple
        model.add(layers.Dense(64, activation='relu', name='pre_output'))
        
        # Múltiples salidas para diferentes predicciones
        lead_quality = layers.Dense(1, activation='sigmoid', name='lead_quality')(model.layers[-1].output)
        investment_propensity = layers.Dense(1, activation='sigmoid', name='investment_propensity')(model.layers[-1].output)
        engagement_likelihood = layers.Dense(1, activation='sigmoid', name='engagement_likelihood')(model.layers[-1].output)
        conversion_probability = layers.Dense(1, activation='sigmoid', name='conversion_probability')(model.layers[-1].output)
        
        # Crear modelo con múltiples salidas
        multi_output_model = keras.Model(
            inputs=model.input,
            outputs=[lead_quality, investment_propensity, engagement_likelihood, conversion_probability]
        )
        
        # Compilar modelo
        multi_output_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss={
                'lead_quality': 'binary_crossentropy',
                'investment_propensity': 'binary_crossentropy',
                'engagement_likelihood': 'binary_crossentropy',
                'conversion_probability': 'binary_crossentropy'
            },
            metrics=['accuracy']
        )
        
        return multi_output_model
    
    def create_conversion_model(self):
        """Crea modelo de predicción de conversión"""
        if not DEEP_LEARNING_AVAILABLE:
            return None
        
        # Modelo LSTM para análisis temporal
        model = keras.Sequential([
            layers.LSTM(128, return_sequences=True, input_shape=(30, 50)),  # 30 días, 50 features
            layers.Dropout(0.3),
            layers.LSTM(64, return_sequences=False),
            layers.Dropout(0.3),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def create_sentiment_model(self):
        """Crea modelo de análisis de sentimientos"""
        if not DEEP_LEARNING_AVAILABLE:
            return None
        
        # Modelo transformer-like para análisis de texto
        model = keras.Sequential([
            layers.Embedding(10000, 128, input_length=500),
            layers.MultiHeadAttention(num_heads=8, key_dim=128),
            layers.GlobalAveragePooling1D(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(3, activation='softmax')  # positivo, neutro, negativo
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def create_segmentation_model(self):
        """Crea modelo de segmentación neural"""
        if not DEEP_LEARNING_AVAILABLE:
            return None
        
        # Autoencoder para segmentación no supervisada
        input_dim = 500
        encoding_dim = 32
        
        # Encoder
        input_layer = layers.Input(shape=(input_dim,))
        encoded = layers.Dense(256, activation='relu')(input_layer)
        encoded = layers.Dense(128, activation='relu')(encoded)
        encoded = layers.Dense(encoding_dim, activation='relu')(encoded)
        
        # Decoder
        decoded = layers.Dense(128, activation='relu')(encoded)
        decoded = layers.Dense(256, activation='relu')(decoded)
        decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)
        
        # Autoencoder completo
        autoencoder = keras.Model(input_layer, decoded)
        encoder = keras.Model(input_layer, encoded)
        
        autoencoder.compile(optimizer='adam', loss='mse')
        
        return {"autoencoder": autoencoder, "encoder": encoder}
    
    async def init_ml_models(self):
        """Inicializa modelos de ML tradicional"""
        try:
            # Ensemble de modelos para lead scoring
            self.ml_models["lead_scorer"] = {
                "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
                "gradient_boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
                "neural_network": MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42),
            }
            
            # Modelo de clustering para segmentación
            self.ml_models["clustering"] = KMeans(n_clusters=8, random_state=42)
            
            # Modelo de reducción de dimensionalidad
            self.ml_models["pca"] = PCA(n_components=50)
            
            self.logger.info("Modelos de ML tradicional inicializados")
            
        except Exception as e:
            self.logger.error(f"Error inicializando modelos ML: {str(e)}")
    
    async def init_nlp_models(self):
        """Inicializa modelos de NLP"""
        try:
            if NLTK_AVAILABLE:
                # Descargar recursos necesarios de NLTK
                try:
                    nltk.download('vader_lexicon', quiet=True)
                    nltk.download('punkt', quiet=True)
                    nltk.download('stopwords', quiet=True)
                    nltk.download('wordnet', quiet=True)
                except:
                    pass
                
                # Analizador de sentimientos
                self.nlp_models["sentiment_analyzer"] = SentimentIntensityAnalyzer()
                
                # Lemmatizer
                self.nlp_models["lemmatizer"] = WordNetLemmatizer()
                
                # Stop words
                self.nlp_models["stop_words"] = set(stopwords.words('english'))
            
            if SPACY_AVAILABLE:
                try:
                    # Cargar modelo de SpaCy
                    self.nlp_models["spacy"] = spacy.load("en_core_web_sm")
                except OSError:
                    self.logger.warning("Modelo SpaCy no encontrado - funcionalidad limitada")
            
            self.logger.info("Modelos de NLP inicializados")
            
        except Exception as e:
            self.logger.error(f"Error inicializando modelos NLP: {str(e)}")
    
    async def init_vectorizers(self):
        """Inicializa vectorizadores de texto"""
        try:
            # TF-IDF Vectorizer
            self.text_vectorizers["tfidf"] = TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 3),
                min_df=2,
                max_df=0.95,
                stop_words='english'
            )
            
            # Count Vectorizer
            self.text_vectorizers["count"] = CountVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                stop_words='english'
            )
            
            # Feature Scaler
            self.feature_scalers["standard"] = StandardScaler()
            
            # Label Encoders
            self.label_encoders = {
                "industry": LabelEncoder(),
                "location": LabelEncoder(),
                "company_size": LabelEncoder(),
                "seniority": LabelEncoder()
            }
            
            self.logger.info("Vectorizadores inicializados")
            
        except Exception as e:
            self.logger.error(f"Error inicializando vectorizadores: {str(e)}")
    
    async def analyze_profile_neural(self, profile_data: Dict[str, Any]) -> NeuralProfileAnalysis:
        """Análisis neural completo de perfil"""
        try:
            profile_id = profile_data.get("profile_id", "")
            self.logger.info(f"🧠 Iniciando análisis neural: {profile_id}")
            
            # Extraer y procesar features
            features = await self.extract_neural_features(profile_data)
            
            # Análisis de personalidad
            personality_analysis = await self.analyze_personality(profile_data, features)
            
            # Análisis de contenido
            content_analysis = await self.analyze_content_neural(profile_data)
            
            # Análisis de comportamiento
            behavior_analysis = await self.analyze_behavior_patterns(profile_data)
            
            # Predicciones neurales
            predictions = await self.make_neural_predictions(features)
            
            # Segmentación neural
            segmentation = await self.perform_neural_segmentation(features)
            
            # Calcular scores principales
            lead_quality_score = await self.calculate_lead_quality_score(features)
            investment_propensity = await self.calculate_investment_propensity(features)
            engagement_likelihood = await self.calculate_engagement_likelihood(features)
            conversion_probability = await self.calculate_conversion_probability(features)
            
            # Crear análisis completo
            analysis = NeuralProfileAnalysis(
                profile_id=profile_id,
                analysis_timestamp=datetime.now(),
                lead_quality_score=lead_quality_score,
                investment_propensity_score=investment_propensity,
                engagement_likelihood_score=engagement_likelihood,
                conversion_probability_score=conversion_probability,
                personality_traits=personality_analysis["traits"],
                communication_style=personality_analysis["communication_style"],
                decision_making_style=personality_analysis["decision_making_style"],
                risk_tolerance=personality_analysis["risk_tolerance"],
                content_sentiment_analysis=content_analysis["sentiment"],
                topic_modeling_results=content_analysis["topics"],
                expertise_areas=content_analysis["expertise"],
                influence_indicators=content_analysis["influence"],
                activity_patterns=behavior_analysis["activity"],
                engagement_patterns=behavior_analysis["engagement"],
                network_analysis=behavior_analysis["network"],
                temporal_behavior=behavior_analysis["temporal"],
                response_time_prediction=predictions["response_time"],
                optimal_contact_time=predictions["optimal_time"],
                preferred_communication_channel=predictions["preferred_channel"],
                message_tone_preference=predictions["tone_preference"],
                neural_segment=segmentation["segment"],
                segment_confidence=segmentation["confidence"],
                similar_profiles=segmentation["similar_profiles"],
                analysis_confidence=self.calculate_analysis_confidence(features),
                model_version="neural_v2.0",
                feature_importance=await self.calculate_feature_importance(features)
            )
            
            # Guardar análisis
            await self.save_neural_analysis(analysis)
            
            self.logger.info(f"✅ Análisis neural completado: {profile_id}")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error en análisis neural: {str(e)}")
            raise
    
    async def extract_neural_features(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae features neurales del perfil"""
        features = {
            "text_features": {},
            "behavioral_features": {},
            "demographic_features": {},
            "network_features": {},
            "temporal_features": {}
        }
        
        try:
            # Features de texto
            text_content = self.combine_text_content(profile_data)
            if text_content and self.text_vectorizers.get("tfidf"):
                try:
                    tfidf_features = self.text_vectorizers["tfidf"].fit_transform([text_content])
                    features["text_features"]["tfidf"] = tfidf_features.toarray()[0]
                except:
                    features["text_features"]["tfidf"] = np.zeros(1000)
            
            # Features demográficas
            features["demographic_features"] = {
                "title_seniority": self.encode_seniority(profile_data.get("title", "")),
                "industry_code": self.encode_industry(profile_data.get("industry", "")),
                "company_size": self.encode_company_size(profile_data.get("company_size", "")),
                "location_tier": self.encode_location(profile_data.get("location", "")),
                "education_level": self.encode_education(profile_data.get("education", [])),
                "experience_years": self.calculate_experience_years(profile_data.get("experience", []))
            }
            
            # Features de comportamiento
            features["behavioral_features"] = {
                "activity_frequency": self.calculate_activity_frequency(profile_data),
                "engagement_rate": self.calculate_engagement_rate(profile_data),
                "content_creation_rate": self.calculate_content_creation(profile_data),
                "network_growth_rate": self.calculate_network_growth(profile_data),
                "response_patterns": self.analyze_response_patterns(profile_data)
            }
            
            # Features de red
            features["network_features"] = {
                "connections_count": profile_data.get("connections_count", 0),
                "followers_count": profile_data.get("followers_count", 0),
                "network_quality": self.calculate_network_quality(profile_data),
                "influence_score": self.calculate_influence_score(profile_data)
            }
            
            # Features temporales
            features["temporal_features"] = {
                "account_age": self.calculate_account_age(profile_data),
                "activity_recency": self.calculate_activity_recency(profile_data),
                "posting_frequency": self.calculate_posting_frequency(profile_data),
                "engagement_trends": self.calculate_engagement_trends(profile_data)
            }
            
            return features
            
        except Exception as e:
            self.logger.error(f"Error extrayendo features neurales: {str(e)}")
            return features
    
    def combine_text_content(self, profile_data: Dict[str, Any]) -> str:
        """Combina todo el contenido de texto del perfil"""
        text_parts = []
        
        # Agregar diferentes campos de texto
        text_fields = ["title", "summary", "headline"]
        for field in text_fields:
            if profile_data.get(field):
                text_parts.append(str(profile_data[field]))
        
        # Agregar experiencia
        if profile_data.get("experience"):
            for exp in profile_data["experience"]:
                if isinstance(exp, dict):
                    text_parts.append(f"{exp.get('title', '')} {exp.get('company', '')}")
        
        # Agregar posts recientes
        if profile_data.get("recent_posts"):
            for post in profile_data["recent_posts"][:5]:  # Limitar a 5 posts
                if isinstance(post, dict) and post.get("content"):
                    text_parts.append(post["content"][:200])  # Limitar longitud
        
        return " ".join(text_parts)
    
    def encode_seniority(self, title: str) -> float:
        """Codifica nivel de seniority"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['ceo', 'cto', 'cfo', 'president', 'founder']):
            return 1.0
        elif any(word in title_lower for word in ['vp', 'vice president', 'director']):
            return 0.8
        elif any(word in title_lower for word in ['manager', 'head', 'lead']):
            return 0.6
        elif any(wor
