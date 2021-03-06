import tensorflow as tf
import numpy as np

def load_csv( filename='game_data.csv'):
    with open(filename, 'r') as f:
        headers = f.readline().replace('/', '_').split(',')
        data = f.readlines()
    return headers, data

class DataClass:


    def __init__(self, headers, data_row):
        data_row = data_row.split(',')
        for name, d in zip(headers, data_row):
            try:
                setattr(self, name.strip(), float(d))
            except:
                setattr(self, name.strip(), d.strip())

    @property
    def win_loss(self):
        return self._win_loss

    @win_loss.setter
    def win_loss(self, val):
        x = val.split('-')
        self._win_loss =  float(x[0])-float(x[1])

    @property
    def opp_win_loss(self):
        return self._opp_win_loss

    @opp_win_loss.setter
    def opp_win_loss(self, val):
        x = val.split('-')
        self._opp_win_loss = float(x[0]) - float(x[1])

    @property
    def home_away(self):
        return self._home_away

    @win_loss.setter
    def home_away(self, val):
        if val.lower() == 'h':
            self._home_away = 2
        elif val.lower() == 'n':
            self._home_away = 1
        else:
            self._home_away = 0
    #@property
    #def outcome(self):
    #    return self._outcome

    #@outcome.setter
    #def outcome(self, value):


data = []
h, d = load_csv()
for row in d:
    data.append(DataClass(h,row))

print(data[0].__dict__)
print(data[0].name)
"""
date, rank, opponent, outcome, team_score, 
opp_score, home/away, rank,name,conf,
win_loss,adjEM,adjO,adjD,adjT,
luck,adjEM,oppO,oppD,noncon_adjEM, 
opp_rank, opp_name, opp_conf, opp_win_loss, opp_adjEM, 
opp_adjO, opp_adjD, opp_adjT, opp_luck, opp_adjEM, 
opp_oppO, opp_oppD, opp_noncon_adjEM

"""


#tf.feature_column.numeric_column(key='rank') #1
feature_columns = [

        tf.feature_column.numeric_column(key='team_score'), #4
        tf.feature_column.numeric_column(key='opp_score'), #5
        tf.feature_column.numeric_column(key='home_away'), #6
        #tf.feature_column.numeric_column(key='conf'), #9
        tf.feature_column.numeric_column(key='win_loss'), #10
        tf.feature_column.numeric_column(key='adjEM'),
        tf.feature_column.numeric_column(key='adjO'),
        tf.feature_column.numeric_column(key='adjD'),
        tf.feature_column.numeric_column(key='adjT'),
        tf.feature_column.numeric_column(key='luck'),
        tf.feature_column.numeric_column(key='oppO'),
        tf.feature_column.numeric_column(key='oppD'),
        tf.feature_column.numeric_column(key='noncon_adjEM'),
        tf.feature_column.numeric_column(key='opp_rank'),
        #tf.feature_column.numeric_column(key='opp_name'),
       # tf.feature_column.numeric_column(key='opp_conf'),
        tf.feature_column.numeric_column(key='opp_win_loss'),
        tf.feature_column.numeric_column(key='opp_adjEM'),
        tf.feature_column.numeric_column(key='opp_adjO'),
        tf.feature_column.numeric_column(key='opp_adjD'),
        tf.feature_column.numeric_column(key='opp_adjT'),
        tf.feature_column.numeric_column(key='opp_luck'),
        tf.feature_column.numeric_column(key='opp_oppO'),
        tf.feature_column.numeric_column(key='opp_oppD'),
        tf.feature_column.numeric_column(key='opp_noncon_adjEM')
        ]




model = tf.estimator.DNNClassifier(
  model_dir='model/',
  hidden_units=[10],
  feature_columns=feature_columns,
  n_classes=2,
  label_vocabulary=['W', 'L'],
  optimizer=tf.train.ProximalAdagradOptimizer(
    learning_rate=0.1,
    l1_regularization_strength=0.001
  ))


import numpy as np

train_features = {


    'team_score': np.array([x.team_score for x in data]),

    'opp_score': np.array([x.opp_score for x in data]), #5
    'home_away': np.array([x.home_away for x in data]), #6
    #'conf': np.array([x.conf for x in data]), #9
    'win_loss': np.array([x.win_loss for x in data]), #10
    'adjEM': np.array([x.adjEM for x in data]),
    'adjO': np.array([x.adjO for x in data]),
    'adjD': np.array([x.adjD for x in data]),
    'adjT': np.array([x.adjT for x in data]),
    'luck': np.array([x.luck for x in data]),

    'oppO': np.array([x.oppO for x in data]),
    'oppD': np.array([x.oppD for x in data]),
    'noncon_adjEM': np.array([x.noncon_adjEM for x in data]),
    'opp_rank': np.array([x.opp_rank for x in data]),
    #'opp_name': np.array([x.opp_name for x in data]),
    #'opp_conf': np.array([x.opp_conf for x in data]),
    'opp_win_loss': np.array([x.opp_win_loss for x in data]),

    'opp_adjO': np.array([x.opp_adjO for x in data]),
    'opp_adjD': np.array([x.opp_adjD for x in data]),
    'opp_adjT': np.array([x.opp_adjT for x in data]),
    'opp_luck': np.array([x.opp_luck for x in data]),
    'opp_adjEM': np.array([x.opp_adjEM for x in data]),
    'opp_oppO': np.array([x.opp_oppO for x in data]),
    'opp_oppD': np.array([x.opp_oppD for x in data]),
    'opp_noncon_adjEM': np.array([x.opp_noncon_adjEM for x in data])
      #'home-goals': np.array([7, 3, 4]),
      #'home-opposition-goals': np.array([3, 8, 6]),
      ## ... for each feature
}

train_labels = np.array([d.outcome for d in data])


train_input_fn = tf.estimator.inputs.numpy_input_fn(
  x=train_features,
  y=train_labels,
  batch_size=500,
  num_epochs=None,
  shuffle=True
  )

model.train(input_fn=train_input_fn, steps=10000, )

#if __name__ == '__main__':
