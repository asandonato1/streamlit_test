def ID3(df, x, y, k): # df --> dataframe; x --> caracteristicas do vetor de entrada; y --> rotulos; k --> tamanho do teste
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score
    from getpass import getpass

    #df = df.apply(preprocessing.LabelEncoder().fit_transform)
    x_treino, x_teste, y_treino, y_teste = train_test_split(x,y, test_size = k)
   # print(x_teste)
    classificador = DecisionTreeClassifier(criterion='entropy', random_state = 100)
    classificador.fit(x_treino, y_treino)

    y_prev = classificador.predict(x_teste)

    res = pd.DataFrame({'real': y_teste, 'prev': y_prev})
    acc = accuracy_score(y_teste, y_prev)
    acc_str = " acc: " + str(acc)
    return res, acc_str


