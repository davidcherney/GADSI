import pandas as pd
from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
data = pd.read_csv('DSI_kickstarterscrape_dataset.csv',encoding='latin9')

#----------------------------- explore -------------------------#
# print(data.info())
#I see 45,957 non-null entries in each of 17 columns no missing data

#Status records successful or failed, this will be encoded to y
# after I get rid of the rows with any status value besides those two

#----------------------------- clean -------------------------#

#drop the columns that are unlikely to contribute to success
#keeping: 
# 'category', 'status', 'goal', 'pledged', 
# 'backers', 'comments', 'duration'
# and note that 'funded percentage' is kept so that the data can be cleaned to 
# exclude viral campaigns, but will need to be dropped
data = data.drop(
                ['project id','name','url','subcategory','location',
                 'funded date','levels','reward levels','updates',
                 ], axis=1)
# print(data.columns)


# drop all rows that have status values other than successful failed
# print(data[['status']].head(5))
data = data[ (data.status == 'successful') | (data.status == 'failed')]
# print(data[['status']].head(5) )

# drop rows for canpaigns that went viral
data = data[ data['funded percentage']<3]
#now that this has been used for data cleaning, also drop it because it it a 
# 100% accuracy proxy for success
data = data.drop(['funded percentage'],axis=1)
# remaining columns:
#keeping: 
# 'category', 'status', 'goal', 'pledged', 
# 'backers', 'comments', 'duration'
print(data.columns)

# keep rows with goals between 500 and 500k $
# print(data.goal.head(10))
data = data[ (500 < data['goal']) & (data['goal']<500_000)]
# print(data.goal.head(10))


#----------------------------- pre-process -------------------------#
# encode non-numerical data
le = preprocessing.LabelEncoder()
cols_to_enumnerate = ['category', 'status']
# print(data[cols_to_enumnerate].head(4))

for col in cols_to_enumnerate:
    data[col] = le.fit_transform(data[col]) 
    # print(le.classes_)

# print(data[cols_to_enumnerate].head(4))
# Looks like it is 1 for success, o for failure

#split the data into train and test sets for model building
y = data['status']
X = data.drop('status', axis=1)
X_train, X_val, y_train, y_val = train_test_split(X,y, test_size=0.2, random_state=42)

#----------------------------- model -------------------------#
clf = LogisticRegression(random_state=1, max_iter=1000).fit(X_train,y_train)
# predict on the validation/development set

#----------------------------- evaluate model -------------------------#
# ok, how accurate was this model?
predictions = clf.predict(X_val)
from sklearn.metrics import accuracy_score 
print(f'Logistic regression model accuracy: {accuracy_score(y_val,predictions)}')


