from flask import Flask
import requests
import json
from flask import jsonify
from flask import request
from requests.auth import HTTPBasicAuth
from flask import render_template
from collections import OrderedDict
app=Flask(__name__)

location_counter=0
co_ordinates_dict=OrderedDict()
cost_check_dict=OrderedDict()
lyft_string=""
uber_string=""
String=""
ubermatrix=[]
lyftmatrix=[]
lyft_roundtrip={}
uber_roundtrip={}
check_roundtrip=False

@app.route('/')
def indexpage():
    return render_template('index.html', LYFT_COST=0.0, LYFT_PATH="lyft", UBER_COST=0.0, UBER_PATH="uber")
@app.route('/form', methods=['POST'])
def form_matrix():
    global lyft_string
    global uber_string
    global location_counter
    global co_ordinates_dict
    global ubermatrix
    global lyftmatrix
    global check_roundtrip
    global String
    location_counter=0
    
    
    obj=UbervsLyft()
    starting_location=request.form['starting_location']
    first_location=request.form['first']
    second_location=request.form['second']
    third_location=request.form['third']
    fourth_location=request.form['fourth']
    fifth_location=request.form['fifth']
    if request.form['check_roundtrip']=="Yes":
        check_roundtrip=True
    else:
        check_roundtrip=False
    
    
    if starting_location:
        location_counter=location_counter+1
        starting_location_parameters=obj.url_parameters(starting_location)
        starting_location_coordinates=obj.get_coordinates(starting_location_parameters)
        if starting_location_coordinates=="Error":
            #print "starting location"
            return "Invalid Address"
        co_ordinates_dict[starting_location]=starting_location_coordinates
    
    if first_location:
        location_counter=location_counter+1
        first_location_parameters=obj.url_parameters(first_location)
        first_location_coordinates=obj.get_coordinates(first_location_parameters)
        if first_location_coordinates=="Error":
            #print "1st location"
            return "Invalid Address"
        co_ordinates_dict[first_location]=first_location_coordinates
        
    if second_location:
        location_counter=location_counter+1
        second_location_parameters=obj.url_parameters(second_location)
        second_location_coordinates=obj.get_coordinates(second_location_parameters)
        if second_location_coordinates=="Error":
            #print "2nd location"
            return "Invalid Address"
        co_ordinates_dict[second_location]=second_location_coordinates
    
    if third_location:
        location_counter=location_counter+1
        third_location_parameters=obj.url_parameters(third_location)
        third_location_coordinates=obj.get_coordinates(third_location_parameters)
        if third_location_coordinates=="Error":
            #print "3rd location"
            return "Invalid Address"
        co_ordinates_dict[third_location]=third_location_coordinates
    
    if fourth_location:
        location_counter=location_counter+1
        fourth_location_parameters=obj.url_parameters(fourth_location)
        fourth_location_coordinates=obj.get_coordinates(fourth_location_parameters)
        if fourth_location_coordinates=="Error":
            #print "4th location"
            return "Invalid Address"
        co_ordinates_dict[fourth_location]=fourth_location_coordinates
        
    if fifth_location:
        location_counter=location_counter+1
        fifth_location_parameters=obj.url_parameters(fifth_location)
        fifth_location_coordinates=obj.get_coordinates(fifth_location_parameters)
        if fifth_location_coordinates=="Error":
            #print "5th location"
            return "Invalid Address"
        co_ordinates_dict[fifth_location]=fifth_location_coordinates
    
    """"
    co_ordinates_dict[starting_location]=starting_location_coordinates
    if first_location:
        co_ordinates_dict[first_location]=first_location_coordinates
    if second_location:
        co_ordinates_dict[second_location]=second_location_coordinates
    if third_location:
        co_ordinates_dict[third_location]=third_location_coordinates
    if fourth_location:
        co_ordinates_dict[fourth_location]=fourth_location_coordinates
    if fifth_location:
        co_ordinates_dict[fifth_location]=fifth_location_coordinates
    """
    
    for i in range(0,location_counter+1):
        lyftmatrix.append([])
        ubermatrix.append([])
    
    ubermatrix[0].append('')
    lyftmatrix[0].append('')
    
    #print co_ordinates_dict
    #print "location counter="
    #print location_counter
    for i in range(0,location_counter):
        #print "i"
        #print i
        ubermatrix[0].append(co_ordinates_dict.keys()[i])
        lyftmatrix[0].append(co_ordinates_dict.keys()[i])
    
    for i in range(0,location_counter):    
        ubermatrix[i+1].append(co_ordinates_dict.keys()[i])
        lyftmatrix[i+1].append(co_ordinates_dict.keys()[i])
        
    lyft_string=obj.lyft_cost()
    ##print "lyft_string"
    ##print lyft_string
    ##print "lyftmatrix="
    ##print lyftmatrix
    ##print "cost_check="
    ##print cost_check_dict
    uber_string=obj.uber_cost()
    """#print lyftmatrix"""
    #print "uber string"
    #print uber_string
    result_string=""
    result_string=obj.Djikstra()
    
    del lyftmatrix[:]
    del ubermatrix[:]
    co_ordinates_dict.clear()
    sending_string=result_string
    sending_split_string=sending_string.split('By Uber')
    sending_lyft_string=sending_split_string[0].split(':')
    sending_lyft_cost_list=sending_lyft_string[1].split(' ')
    sending_lyft_cost=sending_lyft_cost_list[0]
    sending_lyft_path_string=sending_split_string[0].split('Path')
    sending_lyft_path=sending_lyft_path_string[1]
    
    sending_uber_string=sending_split_string[1].split(':')
    sending_uber_cost_list=sending_uber_string[1].split(' ')
    sending_uber_cost=sending_uber_cost_list[0]
    sending_uber_path_string=sending_split_string[1].split('Path')
    sending_uber_path=sending_uber_path_string[1]
    
    return render_template('index.html', LYFT_COST=sending_lyft_cost, LYFT_PATH=sending_lyft_path_string, UBER_COST=sending_uber_cost, UBER_PATH=sending_uber_path)
    
    
class UbervsLyft:
    def __init__(self):
        pass
    
    def url_parameters(self,location):
        address=location.split()
        parameters=""
        for i in address:
            if not parameters:
                parameters=parameters+i
            else:
                parameters=parameters+"+"+i
        return parameters
        
    def get_coordinates(self, parameters):
        url="https://maps.googleapis.com/maps/api/geocode/json?address="+parameters
        geo_json=requests.get(url)
        geo_json=geo_json.json()
        if geo_json['status']=="ZERO_RESULTS":
            return "Error"
        geo_coord=geo_json['results']
        geo_co=geo_coord[0]['geometry']
        co=geo_co['location']
        coordinates=str(co['lat'])+","+str(co['lng'])
        return coordinates
            
    def lyft_cost(self):
        global cost_check_dict
        global location_counter
        global lyftmatrix
        global co_ordinates_dict
        global String
        lyft_token_url = "https://api.lyft.com/oauth/token"
        lyft_token_headers = {'Content-Type':"application/json",'cache-control': "no-cache"}
        lyft_token=requests.post(lyft_token_url,headers=lyft_token_headers,auth=HTTPBasicAuth('I0hVtv9JvVOV', 'YPiHFSAzqn6fznMbB49uKfaNOz9dQ9W9'),json={'grant_type': "client_credentials", 'scope': "public"})
        lyft_token_data=lyft_token.json()
        access_lyft_token=lyft_token_data['access_token']
        
        for i in range(0,location_counter):
            for j in range(0,location_counter):
                if i==j:
                    lyftmatrix[i+1].append(1000)
                    
                else:
                    #start_location_name=co_ordinates_dict.keys()[i]
                    #end_location_name=co_ordinates_dict.keys()[j]
                    start_co=co_ordinates_dict.values()[i]
                    start_co=start_co.split(',')
                    start_co_lat=start_co[0]
                    start_co_lng=start_co[1]
                    end_co=co_ordinates_dict.values()[j]
                    end_co=end_co.split(',')
                    end_co_lat=end_co[0]
                    end_co_lng=end_co[1]    
        
                    lyft_cost_url="https://api.lyft.com/v1/cost?ride_type=lyft&start_lat="+start_co_lat+"&start_lng="+start_co_lng+"&end_lat="+end_co_lat+"&end_lng="+end_co_lng
                    lyft_cost_headers={'Authorization': "Bearer"+" "+access_lyft_token}
                    lyft_cost=requests.get(lyft_cost_url,headers=lyft_cost_headers)
                    lyft_cost_data=lyft_cost.json()
                    lyft_cost_data=lyft_cost_data['cost_estimates']
                    #print "lyft="
                    check=lyft_cost_data[0]['can_request_ride']
                    if not check:
                        #print "Entered"
                        String="\n Service not available for few Destinations "
                        lyftmatrix[i+1].append(10000)
                        continue
                    max_cost=lyft_cost_data[0]['estimated_cost_cents_max']
                    max_cost=float(max_cost)/100
                    min_cost=lyft_cost_data[0]['estimated_cost_cents_min']
                    min_cost=float(min_cost)/100
                    lyft_cost=(max_cost+min_cost)/2
                    #cost_check_dict[start_location_name+end_location_name]=lyft_cost
                    lyftmatrix[i+1].append(lyft_cost)
                    
        if check_roundtrip:
            for i in range(1,location_counter+1):
                lyft_roundtrip[lyftmatrix[i][0]]=lyftmatrix[i][1]          
        return
        
    def uber_cost(self):
        global location_counter
        global ubermatrix
        global co_ordinates_dict
        
        for i in range(0,location_counter):
            for j in range(0,location_counter):
                if i==j:
                    ubermatrix[i+1].append(1000)
                    
                else:
                    flag=0
                    start_co=co_ordinates_dict.values()[i]
                    start_co=start_co.split(',')
                    start_co_lat=start_co[0]
                    start_co_lng=start_co[1]
                    end_co=co_ordinates_dict.values()[j]
                    end_co=end_co.split(',')
                    end_co_lat=end_co[0]
                    end_co_lng=end_co[1]    
        
            
                    uber_cost_url="https://api.uber.com/v1.2/estimates/price?start_latitude="+start_co_lat+"&start_longitude="+start_co_lng+"&end_latitude="+end_co_lat+"&end_longitude="+end_co_lng
                    uber_cost_headers={'Authorization': "Token ydBbvAErXYq192-9DDuxq_5moV41Nw752LR2tTcQ"}
                    uber_cost=requests.get(uber_cost_url,headers=uber_cost_headers)
                    uber_cost_data=uber_cost.json()
                    ##print uber_cost_data
                    for p in range(0,len(uber_cost_data.keys())):
                        if uber_cost_data.keys()[p]=="code":
                            ubermatrix[i+1].append(10000)
                            flag=1
                        #if uber_cost_data['code']:
                        #return uber_cost_data['code']"""
                    if not flag:
                        uber_cost_data=uber_cost_data['prices']
                        for k in uber_cost_data:
                            uber_type=k.get('localized_display_name')
                            if uber_type=="uberX":
                                uber_estimate=k.get('estimate')
                        uber_average=uber_estimate.split('-')
                        uber_min_cost=""
                        uber_max_cost=""
                        for k in uber_average[0]:
                            if k=="$":
                                pass
                            else:
                                uber_min_cost=uber_min_cost+k
                        for k in uber_average[1]:
                            uber_max_cost=uber_max_cost+k
                        uber_cost=(float(uber_max_cost)+float(uber_min_cost))/2
                        ubermatrix[i+1].append(uber_cost)
                    
        if check_roundtrip:
            for i in range(1,location_counter+1):
                uber_roundtrip[ubermatrix[i][0]]=ubermatrix[i][1]
            
        return 
        
    def Djikstra(self):
        global lyft_string
        global location_counter
        global ubermatrix
        global lyftmatrix
        global co_ordinates_dict
        global uber_string
        global String
        lyft_total_cost=0
        uber_total_cost=0
        lyft_path=""
        uber_path=""
        final_string=""
        counter=0
        column=1
        row=1
        min_value=1000
        interim_value=-1
        
        #print "uber_string="
        #print uber_string
        
        #print "lyft string="
        #print lyft_string
        
        #print "lyftmatrix="
        #print lyftmatrix
        if lyft_string:
            lyft_path="Service not available in the specified area"
            lyft_total_cost=0.00
        else:
            while(counter<location_counter-1):
                for i in range(1,location_counter+1):
                    if min_value>lyftmatrix[row][i]:
                        min_value=lyftmatrix[row][i]
                        interim_value=i
                if not lyft_path:
                    lyft_path=lyftmatrix[row][0]+"-"+lyftmatrix[0][interim_value]
                else:
                    lyft_path=lyft_path+"-"+lyftmatrix[0][interim_value]
                if min_value!=1000:
                    lyft_total_cost=lyft_total_cost+min_value
                for j in range(1,location_counter+1):
                    lyftmatrix[j][row]=1000
                column=row
                row=interim_value
                print "column="
                print column
                print "row="
                print row
                lyftmatrix[row][column]=1000
                min_value=1000
                counter=counter+1
                
                
        #print "lyft cost"
        #print lyft_total_cost
            if check_roundtrip:
                for i in range(0,location_counter):
                    if lyftmatrix[0][interim_value]==lyft_roundtrip.keys()[i]:
                        lyft_path=lyft_path+"-"+lyftmatrix[0][1]
                        lyft_total_cost=lyft_total_cost+lyft_roundtrip.values()[i]
                    
        counter=0
        column=1
        row=1
        min_value=1000
        interim_value=-1
        if uber_string:
            uber_path=uber_string
            uber_total_cost=0.00
            #print "uber="
            #print uber_string
        else:
            while(counter<location_counter-1):
                for i in range(1,location_counter+1):
                    if min_value>ubermatrix[row][i]:
                        min_value=ubermatrix[row][i]
                        interim_value=i
                if not uber_path:
                    uber_path=ubermatrix[row][0]+"-"+ubermatrix[0][interim_value]
                else:
                    uber_path=uber_path+"-"+ubermatrix[0][interim_value]
                if min_value!=1000:
                    uber_total_cost=uber_total_cost+min_value
                for j in range(1,location_counter+1):
                    ubermatrix[j][row]=1000
                column=row
                row=interim_value
                ubermatrix[row][column]=1000
                min_value=1000
                counter=counter+1
        #print "uber cost"
        #print uber_total_cost
            
            if check_roundtrip:
                for i in range(0,location_counter):
                    if ubermatrix[0][interim_value]==uber_roundtrip.keys()[i]:
                        uber_path=uber_path+"-"+ubermatrix[0][1]
                        uber_total_cost=uber_total_cost+uber_roundtrip.values()[i]
        
            
        final_string="By Lyft, Cost:"+str(lyft_total_cost)+" "+"Path:"+lyft_path+ String+" "+"By Uber,Cost:"+str(uber_total_cost)+" "+"Path:"+uber_path + String
        return final_string
     
            
        
""""@app.route('/lyft')
def lyftapi():
	#response=requests.get("https://api.lyft.com/v1/lyft_cost?start_lat=37.7772&start_lng=-122.4233&end_lat=37.7972&end_lng=-122.4533")
    lyft_token_url = "https://api.lyft.com/oauth/token"
    lyft_token_headers = {'Content-Type':"application/json",'cache-control': "no-cache"}
    lyft_token=requests.post(lyft_token_url,headers=lyft_token_headers,auth=HTTPBasicAuth('I0hVtv9JvVOV', 'YPiHFSAzqn6fznMbB49uKfaNOz9dQ9W9'),json={'grant_type': "client_credentials", 'scope': "public"})
    lyft_token_data=lyft_token.json()
    access_lyft_token=lyft_token_data['access_token']
    lyft_cost_url="https://api.lyft.com/v1/cost?ride_type=lyft&start_lat=37.329825&start_lng=-121.904980&end_lat=37.335409&end_lng=-121.881093"
    lyft_cost_headers={'Authorization': "Bearer"+" "+access_lyft_token}
    lyft_cost=requests.get(lyft_cost_url,headers=lyft_cost_headers)
    lyft_cost_data=lyft_cost.json()
    return jsonify(lyft_cost_data)
    lyft_cost_data=lyft_cost_data['cost_estimates']
    max_cost=lyft_cost_data[0]['estimated_cost_cents_max']
    max_cost=float(max_cost)/100
    min_cost=lyft_cost_data[0]['estimated_cost_cents_min']
    min_cost=float(min_cost)/100
    lyft_cost=(max_cost+min_cost)/2
    #return str(lyft_cost)

@app.route('/uber')
def uberapi():
    uber_cost_url="https://api.uber.com/v1.2/estimates/price?start_latitude=37.329825&start_longitude=-121.904980&end_latitude=7.335409&end_longitude=-121.881093"
    uber_cost_headers={'Authorization': "Token ydBbvAErXYq192-9DDuxq_5moV41Nw752LR2tTcQ"}
    uber_cost=requests.get(uber_cost_url,headers=uber_cost_headers)
    uber_cost_data=uber_cost.json()
    for p in range(0,len(uber_cost_data.keys())):
        #print uber_cost_data.keys()[p]
    return jsonify(uber_cost_data)
    uber_cost_data=uber_cost_data['prices']
    for i in uber_cost_data:
        uber_type=i.get('localized_display_name')
        if uber_type=="uberX":
            uber_estimate=i.get('estimate')
    uber_average=uber_estimate.split('-')
    uber_min_cost=""
    uber_max_cost=""
    for i in uber_average[0]:
        if i=="$":
            pass
        else:
            uber_min_cost=uber_min_cost+i
    for i in uber_average[1]:
        uber_max_cost=uber_max_cost+i
    uber_cost=(float(uber_max_cost)+float(uber_min_cost))/2
    #return str(uber_cost)
    """
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

