import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from LinearSeparable_Example import perceptron
from matplotlib.colors import ListedColormap

X = np.array([[-0.5,-0,1], [3.5,4.1,-1], [4.5,6,-1], [-2,-2.0,-1], [-4.1,-2.8,-1], [1,3,-1], [-7.1,-4.2,1], [-6.1,-2.2,1],
              [-4.1,2.2,1], [1.4,4.3,1], [-2.4,4.0,1], [-8.4,-5,1]])

def whetherLinearSeparable(X):
    # 提取特征和目标标签
    X_features = X[:, :-1]  # 所有列，除了最后一列
    Y_labels = X[:, -1]  # 只取最后一列作为标签

    # 特征缩放
    sc = StandardScaler()
    X_features = sc.fit_transform(X_features)

    # 训练线性SVM模型
    svm = SVC(C=1.0, kernel='linear', random_state=0)
    svm.fit(X_features, Y_labels)

    # 预测和计算混淆矩阵
    predicted = svm.predict(X_features)
    cm = confusion_matrix(Y_labels, predicted)

    # 绘制混淆矩阵
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Wistia)
    classNames = ['Negative', 'Positive']
    plt.title('SVM Linear Kernel Confusion Matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    tick_marks = np.arange(len(classNames))
    plt.xticks(tick_marks, classNames, rotation=45)
    plt.yticks(tick_marks, classNames)
    s = [['TN', 'FP'], ['FN', 'TP']]

    for i in range(2):
        for j in range(2):
            plt.text(j, i, str(s[i][j]) + " = " + str(cm[i][j]))
    plt.show()
    
    #训练感知器决策边界
    plt.figure()
    X_set, Y_set = X_features, Y_labels
    X1, X2 = np.meshgrid(np.arange(start=X_set[:, 0].min() - 1, stop=X_set[:, 0].max() + 1, step=0.01),
                         np.arange(start=X_set[:, 1].min() - 1, stop=X_set[:, 1].max() + 1, step=0.01))
    Z = perceptron.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape)
    plt.contourf(X1, X2, Z, alpha=0.75, cmap=ListedColormap(('navajowhite', 'darkkhaki')))

    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())

    for i, j in enumerate(np.unique(Y_set)):
        plt.scatter(X_set[Y_set == j, 0], X_set[Y_set == j, 1],
                    color=ListedColormap(('red', 'green'))(i), label=j)

    plt.title('Perceptron Classifier (Decision Boundary)')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.show()

    # 判断线性可分性
    if cm[1, 0] == 0 and cm[0, 1] == 0:
        Y = 1
    else:
        Y = -1

    return Y

# 调用函数
Y = whetherLinearSeparable(X)
if Y == 1:
    print("Y = 1, 该数据集线性可分")
else:
    print("Y = -1, 该数据集非线性可分")