# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:54:12 2017
###KDDCup 2017赛题###
使用GBDT算法，制造特征
@team: GDUTDatamining
@author: johnnywong
"""
import pandas as pd
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import numpy as np
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import ensemble

class KDDCup(object):
    def __init__(self):
        self.name = "<<- User loan forecast match ->>"
        self.result = "submission_travelTime.csv"

    #读取用户信息表 并返回
    def readUserInfo(self):
        user_info_train = readData("train/user_info_train.txt")
        user_info_test = readData("test/user_info_test.txt")
        col_names = ['userid', 'sex', 'occupation', 'education', 'marriage', 'household']
        user_info_train.columns = col_names
        user_info_test.columns = col_names
        user_info = pd.concat([user_info_train, user_info_test])
        user_info.index = user_info['userid']
        user_info.drop('userid',axis=1,inplace=True)
        return user_info

    #读取用户银行账单表 对账单数据求和并返回
    def readBankDetail(self):
        bank_detail_train = readData("train/bank_detail_train.txt")
        bank_detail_test = readData("test/bank_detail_test.txt")
        col_names = ['userid', 'time_bank', 'tradeType', 'tradeMoney', 'incomeTag']
        bank_detail_train.columns = col_names
        bank_detail_test.columns = col_names
        bank_detail_pre = pd.concat([bank_detail_train,bank_detail_test])
        bank_detail = (bank_detail_pre.loc[:,['userid','tradeType', 'tradeMoney']]).groupby(['userid','tradeType']).sum()
        bank_detail = bank_detail.unstack()
        bank_detail.columns = ['income','outcome']
        return bank_detail

    #读取用户的浏览历史 对浏览数据求和并返回
    def readBrowseHistory(self):
        browse_history_train = readData("train/browse_history_train.txt")
        browse_history_test = readData("test/browse_history_test.txt")
        col_names = ['userid', 'time_browse', 'browseData', 'browseTag']
        browse_history_train.columns = col_names
        browse_history_test.columns = col_names
        browse_history_pre = pd.concat([browse_history_train, browse_history_test])
        browse_history = (browse_history_pre.loc[:,['userid','browseData']]).groupby(['userid']).sum()
        return browse_history

    #读取信用卡账单记录 取均值并返回
    def readBillDetail(self):
        bill_detail_train = readData("train/bill_detail_train.txt")
        bill_detail_test = readData("test/bill_detail_test.txt")
        col_names = ['userid', 'time_bill', 'bank_id', 'prior_account', 'prior_repay',
             'credit_limit', 'account_balance', 'minimun_repay', 'consume_count',
             'account', 'adjust_account', 'circulated_interest', 'avaliable_balance',
             'cash_limit', 'repay_state']
        bill_detail_train.columns = col_names
        bill_detail_test.columns = col_names
        bill_detail_pre = pd.concat([bill_detail_train,bill_detail_test])
        bill_detail_pre.drop('bank_id',axis=1,inplace=True)
        bill_detail = bill_detail_pre.groupby(['userid']).mean()
        return bill_detail

    #读取用户发放贷款时间 并返回
    def readLoanTime(self):
        loan_time_train = readData("train/loan_time_train.txt")
        loan_time_test = readData("test/loan_time_test.txt")
        col_names = ['userid','loanTime']
        loan_time_train.columns = col_names
        loan_time_test.columns = col_names
        loan_time = pd.concat([loan_time_train,loan_time_test])
        loan_time.index = loan_time['userid']
        loan_time.drop('userid',axis=1,inplace=True)
        return loan_time

     #读取类别信息
    def readTarget(self):
        target = readData("train/overdue_train.txt")
        target.columns = ['userid', 'label']
        target.index = target['userid']
        target.drop('userid',axis = 1,inplace = True)
        return target

     #新建特征browse, 44维
    def readnBrowse(self):
        browse_train = readData_b('train/n_browse_train.txt')
        browse_test = readData_b('test/n_browse_test.txt')
        browse = pd.concat([browse_train, browse_test])
        browse.index = browse['userid']
        browse.drop('userid', axis = 1, inplace=True)
        return browse

    #新建特征bank，17维
    def readnbank(self):
        bank_train = readData_b('train/n_bank_train.txt')
        bank_test = readData_b('test/n_bank_test.txt')
        bank = pd.concat([bank_train, bank_test])
        bank.index = bank['userid']
        bank.drop('userid', axis = 1, inplace=True)
        return bank

    def readnbill(self):
        bill_train = readData_b('train/n_bill_train.txt')
        bill_test = readData_b('test/n_bill_test.txt')
        bill = pd.concat([bill_train, bill_test])
        bill.index = bill['userid']
        bill.drop('userid', axis = 1, inplace=True)
        return bill

    #利用逻辑斯蒂回归
    def logisticMethod(self):

        user_info = self.readUserInfo()
        # bank_detail = self.readBankDetail()
        bank_detail = self.readnbank()
        # bill_detail = self.readBillDetail()
        bill_detail = self.readnbill()
        loan_time = self.readLoanTime()
        # browse_history = self.readBrowseHistory()
        browse_history = self.readnBrowse()
        target = self.readTarget()

        loan_data = user_info.join(bank_detail,how='outer')
        loan_data = loan_data.join(bill_detail,how='outer')
        loan_data = loan_data.join(browse_history,how='outer')
        loan_data = loan_data.join(loan_time,how='outer')
        loan_data = loan_data.fillna(0.0)

        #对数据进行归一化
        datas = loan_data.values
        datas = preprocessing.scale(datas)

        #更新loan_data里面的数据
        col_names = list(loan_data.columns)
        nums=0
        for col in col_names:
            #把col列的数据替换成归一化处理以后的数据
            loan_data.loc[:,[col]] = datas[:,nums]
            nums += 1

        # #PCA处理
        # pca = PCA(n_components=50)
        # pca.fit(datas.T)
        # ratio = pca.explained_variance_ratio_
        # print 'pca:', ratio
        # print 'sum:', sum(ratio)
        # values = pca.components_.T
        # loan_data = pd.DataFrame(values, columns = range(values.shape[1]), index = loan_data.index)

        #对数据进行划分并且进行训练
        train = loan_data.iloc[0: 55596, :]
        test = loan_data.iloc[55596:, :]
        train_X, test_X, train_y, test_y = train_test_split(train,target,test_size = 0.2,random_state = 0)

        # # Build a forest and compute the feature importances
        # forest = ExtraTreesClassifier(n_estimators=250,
        #                       random_state=0)

        # forest.fit(train_X, train_y)
        # importances = forest.feature_importances_
        # std = np.std([tree.feature_importances_ for tree in forest.estimators_],
        #             axis=0)
        # indices = np.argsort(importances)[::-1]

        # # Print the feature ranking
        # print("Feature ranking:")

        # for f in range(train_X.shape[1]):
        #     print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
        # print train.columns[105], train.columns[0], train.columns[40], train.columns[4], train.columns[36]

        train_y = train_y['label']
        test_y = test_y['label']
        # # 普通的逻辑回归
        # lr_model = LogisticRegression(C = 1.0,penalty = 'l2')
        # lr_model.fit(train_X, train_y)
        # #验证集进行预测
        # pred_test = lr_model.predict(test_X)
        # #对预测结果进行评估
        # print classification_report(test_y, pred_test)
        # #预测测试集数据
        # pred = lr_model.predict_proba(test)

        #采用gradient boosting decision tree
        params = {'n_estimators': 1200, 'max_depth': 3, 'subsample': 0.5,
          'learning_rate': 0.01, 'min_samples_leaf': 1, 'random_state': 3}
        clf = ensemble.GradientBoostingClassifier(**params)
        clf.fit(train_X, train_y)
        pred_test = clf.predict(test_X)
        print classification_report(test_y, pred_test)
        pred = clf.predict_proba(test)


        #对测试集生成结果并存储为csv格式
        result = pd.DataFrame(pred)
        result.index = test.index
        result.columns = ['0', 'probability']
        result.drop('0',axis = 1,inplace = True)
        print result.head(5)
        result.to_csv(self.result)

#数据读取
def readData(filename):
    filepath = './'+filename
    data = pd.read_csv(filepath,header=None)
    return data

def readData_b(filename):
    filepath = './'+filename
    data = pd.read_csv(filepath)
    return data

#开始训练
log_classify = DataCastle()
log_classify.logisticMethod()

