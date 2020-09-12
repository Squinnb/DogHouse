document.addEventListener("DOMContentLoaded", () => {

    //do something here...
   
    let sd = document.querySelector("#searchDiv");
    let hideBtn = document.querySelector("#hideBtn");

    if(hideBtn) {

        hideBtn.addEventListener("click", (e) => {
            console.log(e, e.target)
            if(e.target.innerHTML === "Search") {
                sd.style.display = "block";
                e.target.innerHTML = "Search-"
            } else if(e.target.innerHTML === "Search-") {
                sd.style.display = "none"
                e.target.innerHTML = "Search"
            }
        })
        
    }

   let aboutBtn = document.querySelector("#aboutBtn")
   let aboutDiv = document.querySelector('#aboutDiv')
    if(aboutBtn) {

        aboutBtn.addEventListener("click", (e) => {
            console.log(e, e.target)
            if(e.target.innerHTML === "About") {
                aboutDiv.style.display = "block";
                e.target.innerHTML = "About-"
            } else if(e.target.innerHTML === "About-") {
                aboutDiv.style.display = "none"
                e.target.innerHTML = "About"
            }
        })
        
    }

    
        // dogListButton.addEventListener("click", (e) => {
        //     e.preventDefault()
        //     // Like and unlike post
        //     let dog_id = e.target.value
        //     console.log(dog_id)
        //     fetch(`addDog/${dog_id}`)
        //     .then( (response) => response.json().then( (data) => {
        //         // json() returns a promise... idk why
        //         console.log(data)
        //         if(data.dogListStatus === "added") {
        //             e.target.innerHTML = "Remove from My Dog List";
        //             e.target.nextElementSibling.innerHTML = Number(e.target.nextElementSibling.innerHTML) + 1
        //         }
        //         else if(data.dogListStatus === "removed") {
        //             e.target.innerHTML = "Add to My Dog List";
        //             e.target.nextElementSibling.innerHTML = Number(e.target.nextElementSibling.innerHTML)  - 1
                    
        //         }
        //     }))
        //     .catch( idk => {
        //         console.log("Something's not right fellas...")
        //         console.log("~~~")
        //         console.log(idk)
        //         console.log("~~~")

        //     })

            
        // })
    })

