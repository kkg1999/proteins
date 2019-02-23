import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectKBest,mutual_info_classif
import sys

infile=sys.argv[1]
df=pd.read_csv(infile)

data = df.values[:,:-1]
target = df.values[:,-1]
(row,col)=np.shape(data)

#feature selection
selector = SelectKBest(mutual_info_classif, k='all').fit(data,target)
score=selector.scores_
score=score*1000
ranking=np.argsort(score)
ranking[:]=ranking[::-1]

for loopval in range(1,col):
	temp=ranking[0:loopval]
	datanew=data[:,temp]

	sumbest=0
	mulbest=0
	votbest=0
	mlpbest=knnbest=rfbest=0
	for _ in range(10):
		cross=10
		test_size=(1/cross)
		X_train, X_test, y_train, y_test = train_test_split(datanew, target,stratify=target ,test_size=test_size)

		rf=RandomForestClassifier()
		rf.fit(X_train,y_train)
		predrf=rf.predict_proba(X_test)
		#print("rf: ",rf.score(X_test,y_test))

		knn=KNeighborsClassifier(n_neighbors=10)
		knn.fit(X_train,y_train)
		predknn=knn.predict_proba(X_test)
		#print("knn: ",knn.score(X_test,y_test))
		
		mlp=MLPClassifier(hidden_layer_sizes=(50,25,10 ))
		mlp.fit(X_train,y_train)
		predmlp=mlp.predict_proba(X_test)
		#print("mlp : ",mlp.score(X_test,y_test))
		
		y_pred=[]
		for i in range(len(predrf)):
			l1=predrf[i]
			l2=predknn[i]
			l3=predmlp[i]

			n1=np.array(l1)
			n2=np.array(l2)
			n3=np.array(l3)

			pr=n1+n2+n3
			y_pred.append(1+np.argmax(pr))
			#print(1+np.argmax(pr),y_test[i])

		sumac=accuracy_score(y_pred,y_test)
		#print("sum: ",sumac)

		y_pred=[]
		for i in range(len(predrf)):
			l1=predrf[i]
			l2=predknn[i]
			l3=predmlp[i]

			n1=np.array(l1)
			n2=np.array(l2)
			n3=np.array(l3)

			pr=n1*n2*n3
			y_pred.append(1+np.argmax(pr))
			#print(pr)
			#print(1+np.argmax(pr),y_test[i])

		mulac=accuracy_score(y_pred,y_test)
		#print("mul: ",mulac)

		#majority voting
		y_pred=[]
		for i in range(len(predrf)):
			l1=predrf[i]
			l2=predknn[i]
			l3=predmlp[i]

			n1=np.array(l1)
			n2=np.array(l2)
			n3=np.array(l3)

			n1=n1*((n1==n1.max()).astype('int'))
			n2=n2*((n2==n2.max()).astype('int'))
			n3=n3*((n3==n3.max()).astype('int'))

			pr=n1+n2+n3
			y_pred.append(1+np.argmax(pr))
			#print(pr)
			#print(1+np.argmax(pr),y_test[i])
		
		voteacc=accuracy_score(y_pred,y_test)
		
		rfac=rf.score(X_test,y_test)
		knnac=knn.score(X_test,y_test)
		mlpac=mlp.score(X_test,y_test)

		if rfac>rfbest:
			rfbest=rfac
		if knnac>knnbest:
			knnbest=knnac
		if mlpac>mlpbest:
			mlpbest=mlpac
		if sumac>sumbest:
			sumbest=sumac
			
		if mulac>mulbest:
			mulbest=mulac
		if voteacc>votbest:
			votbest=voteacc

	print(loopval,"%.4f"%rfbest,"%.4f"%knnbest,"%.4f"%mlpbest,"%.4f"%sumbest,"%.4f"%mulbest,"%.4f"%votbest)
