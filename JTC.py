from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

#connecting to local database. This is obvs terrible security. ( discussed as part of lead in to U7)
jtcdb = mysql.connector.connect(user='JTC', password='Journey123',
                            host='127.0.0.1', database='journey_to_cariryn',
                            auth_plugin='mysql_native_password')


#Code runs if index.html called (root)
@app.route('/', methods=['GET', 'POST'])
def index():

    if "Characters" in request.form:
        return render_template('/Characters.html', Race = getrace(), Class = getclass(), Alignment = getalignment(), Armour = getarmour())
    elif "Inventory" in request.form:
        return render_template('/Inventory.html', Player = getplayer(), Item = getitem())
    elif "Items" in request.form:
        return render_template('/Items.html') 
    elif "Encounters" in request.form:
        return render_template('/Encounters.html', Location = getLocation(), NonPlayer = getNonplayer(), Enemies = getEnemy(),Item = getItemEncounter())
    elif "Queries" in request.form:
        return render_template('/Queries.html')
    elif "GSE" in request.form:
        return render_template('/GSE.html', data = getEncounter(), Location = getLocation(), NonPlayer = getNonplayer(), Enemies = getEnemy(),Item = getItemEncounter())
    elif "lifepoints" in request.form:
        return render_template('/lifepoints.html', data= getNonplayerHP()) 
    elif "weight" in request.form:
        return render_template('/weight.html')
    elif "show_items" in request.form:
        return render_template('/show_items.html', data=viewitem())
    else:
        return render_template('/JTC_home.html')


@app.route('/Characters', methods=['GET', 'POST'])
def Character():
  #Takes details from form and crafts a sql statement  
    if "submit" in request.form:
        details = request.form
        FullName = details['FullName'] #Full name originally called Surname
        Char_Race = details['Race']
        Char_Allignment = details['Allignment']
        Char_Class = details['Class']
        Level = details['Level']
        Strength = details['Strength']
        Brawn = details['Brawn']
        Agility = details['Agility']
        Mettle = details['Mettle']
        Craft = details['Craft']
        Insight = details['Insight']
        Resolve = details['Resolve']
        Life = details['Life']
        Char_Armour = details['Armour']
        Age = details['Age']
        cur = jtcdb.cursor()
        cur.execute("INSERT INTO Player(Full_name, RaceID, AllignmentID, ClassID, Level, Strength, Brawn, Agility, Mettle, Craft, Insight, Resolve, Life, ArmourID, Age ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", FullName, Char_Race, Char_Class, Char_Allignment, Level,Strength,Brawn, Agility, Mettle, Craft, Insight, Resolve, Life, Char_Armour, Age)
        jtcdb.commit()
        cur.close()
    elif "cancel" in request.form:
        pass
    return render_template('/JTC_home.html')


@app.route('/Inventory', methods=['GET', 'POST'])
def Inventory():
  #Takes details from form and crafts a sql statement  
    if "submit" in request.form:
        details = request.form
        Player_Name = details['Player']
        Player_Item = details['item']
        cur = jtcdb.cursor()
        cur.execute("INSERT INTO Journey_to_Cariryn.Inventory(PlayerID,ItemID) VALUES (%s,%s)", (Player_Name, Player_Item))
        jtcdb.commit()
        cur.close()
        
    elif "cancel" in request.form:
        pass
    return render_template('/JTC_home.html')


@app.route('/show_items', methods=['GET', 'POST'])
def AllItems():
  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
        details = request.form
        Name = details['Name']
        Cost = details['Cost']
        Load = details['Load']
        cur = jtcdb.cursor()
        jtcdb.commit()
        cur.close()
  elif "cancel" in request.form:
        pass
  return render_template('/JTC_home.html')

@app.route('/lifepoints', methods=['GET', 'POST'])
def Lifepoints():
  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
        details = request.form
        Name = details['Name']
        Life = details['Life']
        cur = jtcdb.cursor()
        jtcdb.commit()
        cur.close()
  elif "cancel" in request.form:
        pass
  return render_template('/JTC_home.html')

@app.route('/GSE', methods=['GET', 'POST'])
def GSE():
  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
        details = request.form
        Location = details['Location']
        NonPlayer = details['NonPlayer']
        Enemy = details['Enemy']
        Item = details['Item']
        cur = jtcdb.cursor()
        jtcdb.commit()
        cur.close()
  elif "cancel" in request.form:
        pass
  return render_template('/JTC_home.html')

@app.route('/Encounters', methods=['GET', 'POST'])
def Encounters():
  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
        details = request.form
        Location = getlocationid(details['Location'])
        Int_Location = Location[0]
        Int_Location = int(Int_Location[0])
        NonPlayer = getnonplayerid(details['NonPlayer']) 
        Int_NonPlayer = NonPlayer[0]
        Int_NonPlayer = int(Int_NonPlayer[0])
        Enemies = getenemyid(details['Enemies']) 
        Int_Enemies = Enemies[0]
        Int_Enemies = int(Int_Enemies[0])
        Item = getitemid(details['Item'])
        Int_Item = Item[0]
        Int_Item = int(Int_Item[0])
        print(Int_Location)
        cur = jtcdb.cursor()
        cur.execute("INSERT INTO journey_to_cariryn.encounter(LocationID, NonplayerID, EnemyID, ItemID) VALUES (%s,%s,%s,%s)", (Int_Location,Int_NonPlayer,Int_Enemies,Int_Item))
        jtcdb.commit()
        cur.close()
  elif "cancel" in request.form:
        pass
  return render_template('/JTC_home.html')


def viewitem():
    cur = jtcdb.cursor()
    cur.execute("SELECT item.Name, item.Cost, item.Load FROM item ORDER BY item.cost DESC")
    data = cur.fetchall()
    return data

def getrace():
    cur = jtcdb.cursor()
    cur.execute("Select RaceID, Name FROM race")
    data = cur.fetchall()
    return data

def getclass():
    cur = jtcdb.cursor()
    cur.execute("Select ClassID, Name FROM classes")
    data = cur.fetchall()
    return data

def getalignment():
    cur = jtcdb.cursor()
    cur.execute("Select AlignmentID, Name FROM alignment")
    data = cur.fetchall()
    return data

def getarmour():    
    cur = jtcdb.cursor()
    cur.execute("Select ArmourID, Name FROM armour")
    data = cur.fetchall()
    return data

def getplayer():    
    cur = jtcdb.cursor()
    cur.execute("Select PlayerID, Full_name FROM player")
    data = cur.fetchall()
    return data

def getitem(): 
    cur = jtcdb.cursor()
    cur.execute("Select ItemID, Name FROM item WHERE ItemID >1 ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def getEncounter(): 
    cur = jtcdb.cursor()
    cur.execute("Select LocationID, NonPlayerID,EnemyID,ItemID FROM encounter WHERE EnemyID = 8")
    data = cur.fetchall()
    return data

def getItemEncounter(): 
    cur = jtcdb.cursor()
    cur.execute("Select ItemID, Name FROM item ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def getEnemy(): 
    cur = jtcdb.cursor()
    cur.execute("Select EnemiesID, Name FROM enemies ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def getLocation(): 
    cur = jtcdb.cursor()
    cur.execute("Select LocationID, Name FROM location ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def getlocationid(name):
    cur = jtcdb.cursor()
    cur.execute("Select LocationID FROM location where `Name`='"+name+"'")
    data = cur.fetchall()
    return data

def getnonplayerid(name):
    cur = jtcdb.cursor()
    cur.execute("Select NonplayerID FROM non_player where `Name`='"+name+"'")
    data = cur.fetchall()
    return data

def getenemyid(name):
    cur = jtcdb.cursor()
    cur.execute("Select EnemiesID FROM enemies where `Name`='"+name+"'")
    data = cur.fetchall()
    return data

def getitemid(name):
    cur = jtcdb.cursor()
    cur.execute("Select ItemID FROM item where `Name`='"+name+"'")
    data = cur.fetchall()
    return data

def getNonplayer(): 
    cur = jtcdb.cursor()
    cur.execute("Select NonplayerID, Name FROM non_player ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def getNonplayerHP(): 
    cur = jtcdb.cursor()
    cur.execute("Select Name, Life FROM non_player WHERE NonplayerID >1 ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def get(): 
    cur = jtcdb.cursor()
    cur.execute("Select Name, Life FROM non_player WHERE NonplayerID >1 ORDER BY Name ASC")
    data = cur.fetchall()
    return data

def getInventory():
    cur = jtcdb.cursor()
    cur.execute("Select * FROM inventory")
    data = cur.fetchall()

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()