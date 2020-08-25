from abc import ABC,abstractmethod
import csv

class StandardizeStatement(ABC):
    
    def __init__(self) -> None:
        self.date=None
        self.transaction_type=None
        self.credit=None
        self.debit=None
        self.transaction_description=None
        self.currency=None
        self.cardname=None
        self.location=None
        self.namechange=None
        self.type_change=None
    
    def template_method(self,inputFile,outputFile):
        with open(outputFile,'w',newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date','Transaction Description','Debit','Credit','Currency','CardName','Transaction','Location'])
            with open(inputFile,'r') as csvfile1:
                csvreader = csv.reader(csvfile1)
                for row in csvreader:
                    string=''.join(row)
                    if len(string)==0:continue
                    else:
                        if self.rowcheck(row): continue
                        self.transaction(row)
                        self.cardName(row)
                        if self.type_change or self.namechange: continue
                        self.func(row)
                        if self.date and self.transaction_type and self.debit and self.credit and self.currency and self.location and self.cardname and self.transaction_description:
                            csvwriter.writerow([self.date,self.transaction_description,self.debit,self.credit,self.currency,self.cardname,self.transaction_type,self.location])
    
    @abstractmethod
    def rowcheck(self):
        pass

    @abstractmethod
    def func(self):
        pass
    
    @abstractmethod
    def cardName(self):
        pass
    
    @abstractmethod
    def transaction(self):
        pass
    

class HDFC(StandardizeStatement):
    def rowcheck(self,row):
        return row[2]=='Amount'

    def func(self,row):
        string = ' '.join(row)
        if string[-1].isnumeric():
            self.credit='0'
            self.debit=row[-1]
            self.date = row[0]
            if self.transaction_type=='Domestic':
                self.transaction_description=row[1]
                self.location=row[1].split()[-1].lower()
                self.currency = 'INR'
            else:
                curr=row[1].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location = curr[-2].lower()
                self.currency = curr[-1]
        elif string[-2]+string[-1]=='cr':
            self.debit='0'
            self.credit = row[-1].split()[0]
            self.date = row[0]
            if self.transaction_type=='Domestic':
                self.transaction_description = row[1]
                self.location = row[1].split()[-1].lower()
                self.currency = 'INR'
            else:
                curr=row[1].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location=curr[-2].lower()
                self.currency = curr[-1].lower()
    
    def transaction(self,row):
        if row[1]=='Domestic Transactions':
            self.transaction_type = 'Domestic'
            self.type_change=True
        elif row[1]=='International Transactions':
            self.transaction_type =  'International'
            self.type_change=True
        else:
            self.transaction_type = self.transaction_type
            self.type_change=False
    
    def cardName(self,row):
        if row[1]=='Rahul':
            self.cardname='Rahul'
            self.namechange=True
        elif row[1]=='Ritu':
            self.cardname='Ritu'
            self.namechange=True
        else:
            self.cardname=self.cardname
            self.namechange=False

class IDFC(StandardizeStatement):
    def rowcheck(self,row):
        return row[2]=='Amount'
    
    def func(self,row):
        string = ''.join(row)
        if string[-2].isnumeric():
            self.credit='0'
            self.debit=row[-2]
            self.date = row[1]
            if self.transaction_type=='Domestic':
                self.transaction_description=row[0]
                self.location=row[0].split()[-1].lower()
                self.currency = 'INR'
            else:
                curr=row[0].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location = curr[-2].lower()
                self.currency = curr[-1]
        elif string[-2]+string[-1]=='cr':
            self.debit='0'
            self.credit = row[-2].split()[0]
            self.date = row[1]
            if self.transaction_type=='Domestic':
                self.transaction_description = row[0]
                self.location = row[0].split()[-1].lower()
                self.currency = 'INR'
            else:
                curr=row[0].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location=curr[-2].lower()
                self.currency = curr[-1].lower()

    def transaction(self,row):
        if row[3]=='Domestic Transactions':
            self.transaction_type = 'Domestic'
            self.type_change=True
        elif row[3]=='International Transactions':
            self.transaction_type =  'International'
            self.type_change=True
        else:
            self.type_change=False

    def cardName(self,row):
        if row[1]=='Rahul':
            self.cardname='Rahul'
            self.namechange=True
        elif row[1]=='Rajat':
            self.cardname='Rajat'
            self.namechange=True
        else:
            self.namechange=False

class ICICI(StandardizeStatement):
    def rowcheck(self,row):
        return row[2]=='Debit'
    
    def func(self,row):
        self.date=row[0]
        if row[-1]=='' and row[-2].isnumeric():
            self.credit='0'
            self.debit=row[-2]
            if self.transaction_type=='Domestic':
                self.transaction_description=row[1]
                self.location=row[1].split()[-1].lower()
                self.currency='INR'
            else:
                curr = row[1].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location=curr[-2]
                self.currency=curr[-1]
        elif row[-1].isnumeric() and row[-2]=='':
            self.debit='0'
            self.credit=row[-1]
            if self.transaction_type=='Domestic':
                self.transaction_description=row[1]
                self.location=row[1].split()[-1].lower()
                self.currency='INR'
            else:
                curr=row[1].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location=curr[-2]
                self.currency=curr[-1]

    def transaction(self,row):
        if row[0]=='Domestic Transactions':
            self.transaction_type = 'Domestic'
            self.type_change=True
        elif row[0]=='International Transactions':
            self.transaction_type =  'International'
            self.type_change=True
        else:
            self.transaction_type = self.transaction_type
            self.type_change=False

    def cardName(self,row):
        if row[2]=='Rahul':
            self.cardname='Rahul'
            self.namechange=True
        elif row[2]=='Raj':
            self.cardname='Raj'
            self.namechange=True
        else:
            self.cardname=self.cardname
            self.namechange=False

class Axis(StandardizeStatement):
    def rowcheck(self,row):
        return row[1]=='Debit'

    def func(self,row):
        self.date=row[0]
        if row[1].isnumeric() and row[2]=='':
            self.debit=row[1]
            self.credit='0'
            if self.transaction_type=='Domestic':
                self.currency='INR'
                self.transaction_description=row[3]
                self.location=row[3].split()[-1].lower()
            else:
                curr=row[3].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location=curr[-2]
                self.currency=curr[-1]
        elif row[1]=='' and row[2].isnumeric():
            self.debit='0'
            self.credit=row[2]
            if self.transaction_type=='Domestic':
                self.currency='INR'
                self.transaction_description=row[3]
                self.location=row[3].split()[-1].lower()
            else:
                curr=row[3].split()
                self.transaction_description=' '.join(curr[:-1])
                self.location=curr[-2]
                self.currency=curr[-1]
            
    def transaction(self,row):
        if row[2]=='Domestic Transactions':
            self.transaction_type = 'Domestic'
            self.type_change=True
        elif row[2]=='International Transactions':
            self.transaction_type =  'International'
            self.type_change=True
        else:
            self.transaction_type = self.transaction_type
            self.type_change=False
    
    def cardName(self,row):
        if row[2]=='Rahul':
            self.cardname='Rahul'
            self.namechange=True
        elif row[2]=='Ritu':
            self.cardname='Ritu'
            self.namechange=True
        else:
            self.cardname=self.cardname
            self.namechange=False

def client_code(abstract_class:StandardizeStatement,inputFile,outputFile) -> None:
    abstract_class.template_method(inputFile,outputFile)


if __name__=='__main__':
    inputFile = input()
    with open(inputFile,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[1]=='Domestic Transactions':
                outputFile='HDFC-Output-Case1.csv'
                client_code(HDFC(),inputFile,outputFile)
                break
            elif row[3]=='Domestic Transactions':
                outputFile='IDFC-Output-Case4.csv'
                client_code(IDFC(),inputFile,outputFile)
                break
            elif row[0]=='Domestic Transactions':
                outputFile='ICICI-Output-Case2.csv'
                client_code(ICICI(),inputFile,outputFile)
                break
            else:
                outputFile='Axis-Output-Case3.csv'
                client_code(Axis(),inputFile,outputFile)
                break              