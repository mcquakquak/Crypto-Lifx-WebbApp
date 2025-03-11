function checkCoin() {
    console.log("sigma sigma boy sigma boy sigma boy vce")
    let coin = document.getElementById("coinInput").value.toLowerCase();
    console.log(coin)

    if (!coin) {
        alert("Its empty dumbo.")
    }

    fetch(`https://f6b1e6be-5a4f-451f-b98e-d0e6080483c9-00-34lxhz2yujhda.spock.replit.dev:3000/change_light/${coin}`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.status === 200) {
                console.log(data)
                let color = data.expectedLightColor;
                let updown;

                if (data.dayChange < 0) {
                    updown = "fallen"
                }
                else {
                    updown = "risen"
                }
                
                document.body.style.backgroundColor = color;
                document.getElementById("resultMessage").innerText = 
                    `The coin ${coin} has ${updown}, it's ${color}!. The light should be ${color}!,`;
            } else {
                document.getElementById("resultMessage").innerText = "Error: Could not fetch data.";
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            document.getElementById("resultMessage").innerText = "Error connecting to server.";
        });
}