### Preprocessing
Preprocessing danych został skonstruowany w postaci pipeline'ów, które składają się z szeregu transformerów. Pierwszym etapem jest usunięcie wartości, które można uznać za nieprawdziwe, na przykład rok urodzenia około 1900 roku. Następnie w procesie tym zawarte są dodatkowe kroki, takie jak uzupełnianie brakujących danych poprzez zastosowanie mediany lub mody, standaryzacja, kodowanie One Hot Encoding oraz zastosowanie techniki upsamplingu ADASYN w celu zrównoważenia klas w przypadku problemów z niezbalansowanymi danymi.

ColumnTransformer zawierający kroki preprocessingu

```python
preprocessor = ColumnTransformer(
    transformers=[
        ('column_dropper', 'drop', ["ID", "Z_CostContact", "Z_Revenue"]),
        ('year_dt', YearFromDtTransformer(), ["Dt_Customer"]),
        ('dumb_year_birth', RemoveDumbYearBirth(), ["Year_Birth"]),
        ('dumb_income', RemoveDumbIncome(), ["Income"]),
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)
```

Przykładowy pipeline dla Dummy klasyfikatora

```python
Pipeline(
    steps=[("preprocessor", preprocessor), ('imputer', SimpleImputer(strategy="median")), ("adasyn", ADASYN()), ("classifier", DummyClassifier())]
)
```

### Screening
W ramach procesu przesiewowego, przetestowano różne modele uczenia maszynowego, w tym:
- XGBoost
- Random Forest
- Decision Tree
- Bagging
- SVM
- KNN
- Logistic Regression
- Base Model

Każdy z tych modeli został oceniony pod kątem jego przydatności w rozwiązaniu konkretnej problematyki, uwzględniając zarówno wydajność predykcyjną, jak i inne istotne metryki oceny, takie jak czas przetwarzania i złożoność modelu.

### Dostrajanie modeli

Spośród wymienionych modeli wybrano dwie architektury, które wyróżniały się najwyższą wartością sensitivity, czyli metryką wybraną przez nas jako kluczową w rozwiązywanym problemie. Wybrana metryka jest istotna z uwagi na nasze podejście, które polega na maksymalizacji liczby klientów będących potencjalnym celem kampanii reklamowej.

Wybrane architektury to:

- XGBoost
- Regresja Logistyczna

Obie te architektury wykazały się wysoką czułością, co sprawia, że są odpowiednie do naszych potrzeb, umożliwiając identyfikację większej liczby potencjalnych klientów docelowych.

| Model              | Accuracy  | F1 Score | Sensitivity | Specificity |
|--------------------|-----------|----------|-------------|-------------|
| Regresja Logistyczna | 0.8147    | 0.5744   | 0.7887      | 0.4516      |
| XGBoost            | 0.8839    | 0.6000   | 0.5493      | 0.6610      |


Model XGBoost dostrajany był z wykorzystaniem optymalizacji Bayesowskiej, natomiast w procesie dostrajania regresji logistycznej wykorzystana została siatka losowa.

Definicja pipeline'u zwracającego scoring dla optymalizacji Bayesowskiej

```python
def pipeline_cv_score(parameters):
    parameters = parameters[0]
    # Construct the pipeline with given hyperparameters
    pipeline = Pipeline([('preprocessor', preprocessor),
        ('imputer', SimpleImputer(strategy="median")),
        ('sampling', ADASYN()),  # Your preprocessor pipeline
        ('classifier', xgb.XGBClassifier(
            max_depth=int(parameters[0]),
            min_child_weight=int(parameters[1]),
            subsample=parameters[2],
            colsample_bytree=parameters[3],
            n_estimators=int(parameters[4]),
            learning_rate=parameters[5],
            random_state=2115))
    ])
    # Evaluate the pipeline using cross-validation
    score = cross_val_score(pipeline, X_train, y_train, scoring=make_scorer(recall_score), cv=5).mean()
    return score
```

Definicja przestrzeni przeszukiwania i uruchomienie optymalizatora

```python
# Define the search space for Bayesian optimization
bayesian_opt_bounds = [
    {'name': 'max_depth', 'type': 'discrete', 'domain': (3, 15)},
    {'name': 'min_child_weight', 'type': 'discrete', 'domain': (1, 5, 10)},
    {'name': 'subsample', 'type': 'continuous', 'domain': (0.5, 1.0)},
    {'name': 'colsample_bytree', 'type': 'continuous', 'domain': (0.5, 1.0)},
    {'name': 'n_estimators', 'type': 'discrete', 'domain': (100, 200, 300, 400)},
    {'name': 'learning_rate', 'type': 'continuous', 'domain': (0.01, 0.2)}
]
# Initialize and run Bayesian optimization
optimizer = BayesianOptimization(
	f=pipeline_cv_score, domain=bayesian_opt_bounds, model_type='GP',
	acquisition_type='EI', max_iter=25
    )
optimizer.run_optimization()
```

Uczenie modelu z wykorzystaniem optymalnych hiperparametrów

```python
# Initialize and train the model with the best parameters
best_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', xgb.XGBClassifier(
        max_depth=int(best_params_bayesian[0]),
        min_child_weight=int(best_params_bayesian[1]),
        subsample=best_params_bayesian[2],
        colsample_bytree=best_params_bayesian[3],
        n_estimators=int(best_params_bayesian[4]),
        learning_rate=best_params_bayesian[5],
        random_state=2115
    ))
])
best_pipeline.fit(X_train, y_train)
```