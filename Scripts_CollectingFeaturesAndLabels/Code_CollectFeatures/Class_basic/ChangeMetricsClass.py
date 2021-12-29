
class ChangeMetricsClass(object):
    
    instanceName = '';
    LOC = 0;
    LOC_touched = 0;
    Number_of_Revisions = 0;
    Fix_Count = 0;
    Authors = 0;
    LOC_added = 0;
    Max_LOC_added = 0;
    Average_LOC_added = 0;
    Churn = 0;
    Max_Churn = 0;
    Average_Churn = 0;
    Change_Set_Size = 0;
    Max_Change_Set_Size = 0;
    Average_Change_Set_Size = 0;
    Release_Length = 0;
    Weighted_Release_Length = 0;
    
    def __init__(self):
        self.instanceName = '';
        self.LOC = 0;
        self.LOC_touched = 0;
        self.Number_of_Revisions = 0;
        self.Fix_Count = 0;
        self.Authors = 0;
        self.LOC_added = 0;
        self.Max_LOC_added = 0;
        self.Average_LOC_added = 0;
        self.Churn = 0;
        self.Max_Churn = 0;
        self.Average_Churn = 0;
        self.Change_Set_Size = 0;
        self.Max_Change_Set_Size = 0;
        self.Average_Change_Set_Size = 0;
        self.Release_Length = 0;
        self.Weighted_Release_Length = 0;
        
    ### 将度量转成一行
    def metrics2list(self):
        list_oneInstance = [self.instanceName,self.LOC,self.LOC_touched,self.Number_of_Revisions,self.Fix_Count,
                            self.Authors,self.LOC_added,self.Max_LOC_added,self.Average_LOC_added,self.Churn,
                            self.Max_Churn,self.Average_Churn,self.Change_Set_Size,self.Max_Change_Set_Size,
                            self.Average_Change_Set_Size,self.Release_Length,self.Weighted_Release_Length,];
        return list_oneInstance;
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
