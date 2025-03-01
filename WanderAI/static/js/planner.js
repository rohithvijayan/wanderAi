const form=document.getElementById("itinerary-form")
const itinerary=document.getElementById("itinerary-content")
const location_span=document.getElementById("location")
const itinerary_section=document.getElementById("itinerary-section")
const spinner=document.getElementById("spinner")
const gen_btn=document.getElementById("generate-btn")
gen_btn.addEventListener("click",()=>{
    itinerary_section.style.display="block"
    showSpinner()
})
function showSpinner(){
    console.log("spinner started..")
    spinner.style.dipslay="flex"
}
function hideSpinner(){
    console.log("spinner stopped..")
    spinner.style.display="none"
}
form.addEventListener("submit",async (e)=>{
    e.preventDefault();
    //collect data from form
    const data={'destination':form.destination.value,
        'pax':form.persons.value,
        'dept_date':form.departure_date.value,
        'arrival_date':form.arrival_date.value,
        'arrival_transport':form.arrival_transport.value,
        'type_of_trip':form.journey_type.value,
        'budget':form.budget.value,
    };
    console.log(data)
    console.log(data.arrival_transport)
    itinerary_section.style.display="block"
    spinner.style.display="flex"
    //console.log('data=',data)
    //sending data to server
    try{
        const response=await fetch('http://127.0.0.1:8000/api/submit_data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // This ensures the server knows it's JSON
            },
            body: JSON.stringify(data), // Ensure formData is serialized to JSON
        })
        console.log("status of post is",response.status)

    }
    catch(error){
        console.log("An error occurred, Unable to submit data",error)
    }
    setTimeout(()=>{
        fetch('http://127.0.0.1:8000/api/get_itinerary/')
        .then(response=>response.json())
        //.then(data=>console.log('returned json is=',data))
        .then(data=>{
            console.log(data.destination)
            hideSpinner();
            location_span.innerText=data.destination
            itinerary.innerHTML=data.itinerary
        })
    },2000)//fetching response from server
    

})
const collapse_btn=document.getElementById("collapse-btn")
collapse_btn.addEventListener("click",()=>{
    if(collapse_btn.innerText=='Show Itinerary'){
        collapse_btn.innerText='Hide Itinerary'
    }
    else{
        collapse_btn.innerText='Show Itinerary'
    }
})
//colappsible
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    //this.classList.toggle("active");
    
    if (itinerary.style.display === "block") {
      itinerary.style.display = "none";
    } else {
      itinerary.style.display = "block";
    }
  });
}