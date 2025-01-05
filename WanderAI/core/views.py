from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import google.generativeai as genai
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
model=genai.GenerativeModel("gemini-1.5-flash")
trip_details={}
trip_data={"destination":"","pax":"","arrival_date":"","departure_date":"","type_of_trip":"","budget":""}
# Create your views here.
def home(request):
    return render(request,'index.html')

def planner(request):
    return render(request,'planner.html')
@csrf_exempt
def submit_data(request):
        if request.method == 'POST':
            global trip_details
            global trip_data
            print(request)
            data=json.loads(request.body)
            #print(data)
            destination=data.get('destination')
            pax=data.get('pax')
            departure_date=data.get('dept_date')
            arrival_date=data.get("arrival_date")
            type_of_trip=data.get('type_of_trip')
            budget=data.get('budget')
            trip_data={"destination":destination,"pax":pax,"arrival_date":arrival_date,"departure_date":departure_date,"type_of_trip":type_of_trip,"budget":budget}
            trip_details=f'The destination is {destination} for pax of {pax},Starting from {arrival_date} till {departure_date}.\nIt is a {type_of_trip} with a budget of {budget}.'
            #print(trip_details)
            #Get_itinerary()
            return JsonResponse({'message':"data successfulyy submited"})


@csrf_exempt
def Get_itinerary(request):
    global trip_data
    #print("returned json is- ",trip_details)
    itinerary=generate_itinerary(request)
    #print(trip_data)
    return JsonResponse({'itinerary':itinerary,'destination':trip_data['destination']})

def generate_itinerary(request):
    global trip_data
    print('TRIP DATA OBJCET=',trip_data)
    output_structure='''Day 1 (Feb 25): Arrival in New York City
        Arrival: Arrive at JFK Airport.
        Transportation: Take a budget-friendly shuttle or subway to your accommodation (budget hotel or hostel in Queens or Brooklyn).
        Activities:
        Explore Times Square in the evening (free).
        Grab affordable street food (hot dogs, pretzels).
        Take a leisurely walk in the neighborhood.
        Day 2: Explore New York City
        Morning:
        Visit Central Park (free entry).
        Walk to Bethesda Terrace and Bow Bridge.
        Afternoon:
        Stroll the High Line, a park built on a former elevated rail line (free).
        Explore Chelsea Market for window shopping and affordable snacks.
        Evening:
        Walk across the Brooklyn Bridge and enjoy skyline views (free).
        Day 3: New York City Sightseeing
        Morning:
        Visit the 9/11 Memorial (free entry).
        Walk through Wall Street and view the Charging Bull.
        Afternoon:
        Take the Staten Island Ferry for free views of the Statue of Liberty and Ellis Island.
        Explore Battery Park.
        Evening:
        Explore Chinatown and enjoy affordable meals like dumplings or noodles.
        Day 4: Travel to Washington, D.C.
        Transportation: Take an affordable bus or Amtrak train to Washington, D.C. (4-5 hours).
        Arrival: Check into a budget hotel or hostel.
        Evening:
        Visit the Lincoln Memorial and the Reflecting Pool (free).
        Walk around the National Mall.'''
    prompt=f'''Create a detailed, {trip_data["budget"]}-budget {trip_data["type_of_trip"]} travel itinerary for {trip_data["pax"]} people visiting the {trip_data["destination"]} from {trip_data["arrival_date"]}, to {trip_data["departure_date"]}. The itinerary should include a mix of sightseeing, outdoor activities, cultural experiences, and local food exploration,with a focus on {trip_data["type_of_trip"]} Mood for the trip. Please break the itinerary down by day, starting with Day 1 (arrival){trip_data["arrival_date"]} and continuing through to last day(departure){trip_data["departure_date"]}. For each day, include a concise list of things to do, with a focus on  {trip_data["budget"]}-budget activities. The itinerary should also include travel details like transportation (bus, train, or affordable flights) between cities.The Desired response structre is {output_structure}.STRICLY AVOID USAGE OF ANY SYMBOLS.STRICLY DO NOT INCLUDE ```html in the response.THE LINES LIKE 'Day 1 February 25 Arrival in New York City' should be a <h3> element and the text following the corresponding day like 'Arrival: Arrive at JFK Airport.
        Transportation: Take a budget-friendly shuttle or subway to your accommodation (budget hotel or hostel in Queens or Brooklyn).
        Activities:
        Explore Times Square in the evening (free).
        Grab affordable street food (hot dogs, pretzels).
        Take a leisurely walk in the neighborhood.' should be within a <ul> such that each appears one below other .STRICLY AVOID THE 'Note: This itinerary assumes you have pre-booked your accommodation in Varkala. Transportation costs within Varkala can be managed by using auto-rickshaws or walking, which are affordable options. The budget can be adjusted by choosing accommodation and activities that suit your preferences. Always negotiate prices beforehand, especially for taxis and massages. February is a pleasant time to visit Varkala, but it is advisable to check the weather forecast closer to your travel dates. ' Part in response instead end with a 'We Hope To Give You A Memmorable Vacation !' as a <h4> and center it in the div'''
    response=model.generate_content(prompt)
    return response.text
