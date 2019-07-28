from gurobipy import *
import data_read_MRCPSP
import  pandas as pd
import random
import matplotlib.pyplot as plt
import  numpy as np
import  copy
import time

def MutiObj(model, where):
    if where == GRB.Callback.MULTIOBJ:
        print (".................")
        print(model.cbGet(GRB.Callback.MULTIOBJ_OBJCNT))
        input()
    if where == GRB.Callback.MIPNODE:
        print ("*****************")
        print (model.cbGet(GRB.Callback.MIPNODE_NODCNT))
        input()


class Instance():
    def __init__(self):
        self.successors=[]
        self.job_num_successors=[]
        self.job_predecessors = []
        self.job_successors=[]
        self.job_model_resource={1:{1:[0,0,0,0],2:[0,0,0,0],3:[0,0,0,0]},16:{1:[0,0,0,0],2:[0,0,0,0],3:[0,0,0,0]}}
        self.job_model_duration={1:{1:0,2:0,3:0},16:{1:0,2:0,3:0}}
        self.resource_capacity=[]
        self.number_job =None
        self.number_renewable_resources = None
        self.number_unrenewable_resources = None
        self.resource_capacity = None
        self.upper_bound=228
        self.qim={}
        self.Ofs={}    #固定订购成本
        self.CRr=[5,7]
        self.CNfks = {}
        self.Icf = [200,300]
        self.Ift_1=[]
        self.Ift_2=[]
    def loadData(self,file):
        data_read_MRCPSP.dataStore(self, file)
        qim_df=pd.read_excel("./data/qim.xlsx",columns=[1,2,3])
        self.qim=qim_df.to_dict(orient="index")

        Ofs_df=pd.read_excel("./data/Ofs.xlsx")
        self.Ofs=Ofs_df.to_dict(orient="index")


        CNfks_df=pd.read_excel("./data/CNfks.xlsx")
        for s in range(7):
            F_dic = {}
            K_dic={}
            for r1 in range(2):
                for k in range(3):
                    if r1==0:
                        K_dic[k]=CNfks_df[k+1][2*s]
                    if r1==1:
                        K_dic[k] = CNfks_df[k + 1][2 * s+1]
                K_dicb=copy.copy(K_dic)
                F_dic[r1]=K_dicb
            self.CNfks[s]=F_dic



    def Gurobi_RSPSP_J14(self):
        # Set the upper bound Completion Time of the project
        # we set T=100 when you solve the J30 problem

        F=2 #numbers of materials
        S=7 #numbers of suppliers
        K=3 # interval of discount
        T=50
        Mo=3
        DL=15
        p1=12   #延误成本
        p2=6    #成品库存成本
        self.Ift_1=[0 for _ in range(T)]
        self.Ift_2 = [0 for _ in range(T)]





        # Initial the gurobi model
        m = Model()
        #add variables xjt note that j activity start at time t
        x = m.addVars(self.number_job,Mo,T,vtype=GRB.BINARY, name='x')
        # y = m.addVars(F, K,S, T, vtype=GRB.BINARY, name='y')
        # z = m.addVars(F, K,S, T,self.number_job,vtype=GRB.BINARY, name='z')
        Qfkst = m.addVars(F, K, S, T, vtype=GRB.INTEGER, name='Qfkst')



        for t in range(10,T-10):    #项目开始前的预留时间10天
            use_unrenew=0
            for job in range(1,self.number_job-1):
                for jm4 in range(Mo):
                    use_unrenew+=(self.job_model_resource[job+1][jm4+1][0+2])*x[job,jm4,t-1]
                    # (self.job_model_resource[job+1][jm4+1][f+2]/self.job_model_duration[job+1][jm4+1])*sum(x[job,jm4,tt-1] for tt in range(t,t+self.job_model_duration[job+1][jm4+1]))
            L=0 #int(np.random.normal(5,0.5))
            self.Ift_1[t]=self.Ift_1[t-1]+sum(Qfkst[0,k,s,t-L] for k in range(K) for s in range(S))-use_unrenew
        for t2 in range(T):
          m.addConstr( self.Ift_1[t2]>=sum(self.job_model_resource[j+1][jm+1][2+0]*x[j,jm,t2] for j in range(self.number_job) for jm in range(Mo)) ,name='inven'+str(0)+str(t2))

        for t in range(10,T-10):    #项目开始前的预留时间10天
            use_unrenew=0
            for job in range(1,self.number_job-1):
                for jm4 in range(Mo):
                    use_unrenew+=(self.job_model_resource[job+1][jm4+1][1+2])*x[job,jm4,t-1]
                    # (self.job_model_resource[job+1][jm4+1][f+2]/self.job_model_duration[job+1][jm4+1])*sum(x[job,jm4,tt-1] for tt in range(t,t+self.job_model_duration[job+1][jm4+1]))
            L=0 #int(np.random.normal(5,0.5))
            self.Ift_2[t]=self.Ift_2[t-1]+sum(Qfkst[1,k,s,t-L] for k in range(K) for s in range(S))-use_unrenew
        for t2 in range(T):
          m.addConstr( self.Ift_2[t2]>=sum(self.job_model_resource[j+1][jm+1][2+1]*x[j,jm,t2] for j in range(self.number_job) for jm in range(Mo)) ,name='inven'+str(1)+str(t2))



        # Set the obj1 which means the minmize the Completion Time
        obj1=0
        for t in range(T):
            for jm1 in range(Mo):
                obj1+=x[self.number_job-1,jm1,t]*t

        obj2=0
        for i in range(self.number_job):
            for jm in range(Mo):
                for t in range(T):
                   obj2+=self.qim[i][jm+1]*x[i,jm,t]

        obj31=0
        for s in range(S):
            for f in range(F):
                for k in range(K):
                    for t in range(T):
                        obj31+=(self.Ofs[s][f]+self.CNfks[s][f][k]*Qfkst[f,k,s,t])   #*y[f,k,s,t]
        obj32=0
        for i in range(self.number_job):
            for r in range(self.number_renewable_resources):
                for jm2 in range(Mo):
                    for t in range(T):
                        obj32+=self.job_model_resource[i+1][jm2+1][r]*x[i,jm2,t]*self.CRr[r]
        # obj33=0
        # for f in range(F):
        #     for t in range(T):
        #         obj33+=self.Ift[f][t]*self.Icf[f]
        obj33 = 0

        for t in range(T):
            obj33 += self.Ift_1[t] * self.Icf[0]+self.Ift_2[t] * self.Icf[1]



        obj34=0
        for jm3 in range(Mo):
            for t in range(T):
                if t>=DL:
                    obj34+=(t-DL)*x[self.number_job-1,jm3,t]*p1
                else:
                    obj34+=(DL-t)*x[self.number_job-1,jm3,t]*p2
        obj3=obj31+obj32+obj33+obj34

        m.setObjectiveN(obj1,index=0, priority=1, abstol=0, reltol=0, name='obj1')   #时间
        m.setObjectiveN(-obj2, index=1, priority=2, abstol=0, reltol=0, name='obj2') #质量
        m.setObjectiveN(obj33, index=2, priority=3, abstol=0, reltol=0, name='obj3')  #成本


        # Constraint only can be done once
        for i in range(self.number_job):
            m.addConstr(sum(x[i,jm,t] for t in range(T) for jm in range(Mo))==1,name="ccc")

        # Timing constraint
        for i in range(self.number_job):
            if len(self.job_predecessors[i]) !=0:
                for j in self.job_predecessors[i]:
                    sum_ti=0
                    sum_tj=0
                    for jm in range(Mo):
                        for t0 in range(T):
                            sum_ti+=x[i,jm,t0]*t0
                        for t1 in range(T):
                            sum_tj+=x[j-1,jm,t1]*(t1+self.job_model_duration[j][jm+1])
                        m.addConstr(sum_ti>=sum_tj)

        # Resource constraint
        for k in range(self.number_renewable_resources):
            for t3 in range(40):
                use_resource=0
                for j in range(self.number_job):
                    for jm2 in range(Mo):
                        use_resource+=sum(x[j,jm2,tt] for tt in range(max(0,t3-self.job_model_duration[j+1][jm2+1]),t3))*self.job_model_resource[j+1][jm2+1][k]
                m.addConstr(self.resource_capacity[k]-use_resource>=0)
        use_un=[]
        for r in range(self.number_unrenewable_resources):
            use_unresource=0
            for j in range(self.number_job):
                for t4 in range(T):
                    use_unresource+=sum(x[j,mm,t4]*self.job_model_resource[j+1][mm+1][2+r] for mm in range(Mo))
            m.addConstr(self.resource_capacity[r+2]-use_unresource >=0)

        m.setParam("TimeLimit", 1800)
        m.write('lnear_model111.lp')
        m.optimize()


        # Get the solution
        start=[]
        model=[]
        count=0
        for v in m.getVars():
            if v.x!=0 and count<=15:
                print('%s %g' % (v.varName, v.x))
                a=eval(v.varName[1:])
                model.append(a[1]+1)
                start.append(a[2])
                count+=1
            a=0
            if v.x and count > 15:
                print(v.varName,v.x)


        finish=[]
        count=0
        for start1 in start:
            finish.append(start1+self.job_model_duration[count+1][model[count]])
            count+=1

        # print('Obj: %g' % m.objVal)
        print('model',model)
        print('start',start)
        print("finish",finish)
        un1=0
        un1_list=[]
        un2=0
        un2_list=[]
        for i in range(self.number_job):
            un1+=self.job_model_resource[i+1][model[i]][2]
            un1_list.append(self.job_model_resource[i+1][model[i]][2])
            un2+=self.job_model_resource[i+1][model[i]][3]
            un2_list.append(self.job_model_resource[i+1][model[i]][3])
        print(un1_list,"\n",un2_list)
        print(un1,un2)
        for i in range(3):
            m.setParam(GRB.Param.ObjNumber, i)
            print('Obj%d = ' % (i + 1), m.ObjNVal)



        return start,finish
