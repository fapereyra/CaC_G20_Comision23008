document.querySelector('#buscar').addEventListener("click", getPokemon);

function getPokemon(){
    const name=document.querySelector("#nombrePokemon").value;

    fetch (`https://pokeapi.co/api/v2/pokemon/${name}`)
    .then((response)=>response.json())
    .then((data)=>{
        document.querySelector(".cuadroPokemon").innerHTML=`
            <div>
                <img
                    src='${data.front_default}';
                    alt="${data.name}";
                />
            </div>
            <div class="infoPokemon">
                <h1>${data.name}</h1>
                <p>Wight: ${data.weight}</p>
            </div>
        `;
    })
    /*.catch((err)=>{
        console.log("No existe Pokemon",err);
    })
    e.preventDefault();*/
}
getPokemon();

