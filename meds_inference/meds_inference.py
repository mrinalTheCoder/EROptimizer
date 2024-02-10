import numpy as np
import tensorflow as tf

def infer(model, inputs, med_cols):
    inputs = np.expand_dims(np.array(inputs), axis=0)
    preds = model.predict(inputs)[0]
    to_admit = preds[0] > 0.5
    preds = preds[1:]
    meds_list = [med_cols[i] for i in range(len(preds)) if preds[i] > 0.5]
    return to_admit, meds_list

def main():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(483),
        tf.keras.layers.Dense(300, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(200, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(49, activation="sigmoid")
    ])
    model.load_weights("meds_inference/meds_model.h5")
    with open("meds_inference/med_cols.txt") as f:
        med_cols = list(map(lambda x: x[:-1], f.readlines()))
    inputs = [0.35]
    inputs.extend([0 for i in range(482)])
    print(infer(model, inputs, med_cols))

if __name__ == "__main__":
    main()