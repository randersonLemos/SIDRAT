import tensorflow as tf
print(tf.__version__)


class Neural_Network:
    def __init__(self, input_shape, nneurons, batchsize, epochs):
        self.input_shape = input_shape
        self.nneurons = nneurons
        self.batchsize = batchsize
        self.epochs = epochs
        

        self._processing()


    def _processing(self):
        model = tf.keras.Sequential(
            [
            tf.keras.layers.Flatten(input_shape=self.input_shape), # input_shape: (a, b)
            #tf.keras.layers.Dense(128, activation=tf.nn.relu),
            tf.keras.layers.Dense(self.nneurons, activation=tf.nn.relu),
            tf.keras.layers.Dense( 1, activation=tf.nn.sigmoid),
            ]
        )

        model.compile(
            optimizer=tf.keras.optimizers.Adam(),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        self.model = model


    def train(self, X, y):

        #count = self.epochs
        #
        #import pdb; pdb.set_trace()

        #while count:
        #    index = np.arange(len(X))
        #    np.random.shuffle(index)
        #    X.to_numpy()[index,:]
        #    self.model.fit(X.to_numpy()[index,:], y.to_numpy()[index], epochs=1)
        #    count -= 1

        #self.model.fit(X.to_numpy(), y.to_numpy(), epochs=self.epochs, batch_size=5, verbose=2)
        self.model.fit(  X.to_numpy()
                       , y.to_numpy()
                       , epochs=self.epochs
                       , batch_size=self.batchsize
                       , verbose=2
                      )


    def classify(self, X):
        return self.model.predict(X)


from sklearn.ensemble import RandomForestClassifier


class Random_Forest:
    def __init__(self, n_estimators):
        self.n_estimators = n_estimators

        self._processing()


    def _processing(self):
        # Create the model with 100 trees
        model = RandomForestClassifier(  n_estimators=100
                                       , bootstrap=True
                                       , max_features='auto'
                                       , verbose=1
                                      )
        self.model = model


    def train(self, X, y):
        # Fit on training data
        self.model.fit(X, y)


    def classify(self, X):
        return  self.model.predict_proba(X)[:, 1]
