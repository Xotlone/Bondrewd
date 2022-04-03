import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from memory_profiler import memory_usage

x_train = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y_train = np.array([
    [0],
    [1],
    [1],
    [0]
])
model = Sequential()
model.add(Dense(4, 'relu', input_dim=2))
model.add(Dense(1, 'sigmoid'))
model.summary()

opt = Adam(.1)
model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100)
print(model.predict(x_train))
print(memory_usage(max_usage=True))
