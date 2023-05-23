document.querySelector('#buscar').addEventListener("click", getPokemon);

function getPokemon() {
    const idPokemon = document.querySelector("#idPokemon").value;

    fetch(`https://pokeapi.co/api/v2/pokemon/${idPokemon}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            document.querySelector(".cuadroPokemon").innerHTML = `
            <div>
                <img
                    src='${data.sprites.other["official-artwork"].front_default}';
                    alt="${data.name}";
                />
            </div>
            <div class="infoPokemon">
                <h1>${data.name}</h1>
                <p>Weight: ${data.weight}</p>
            </div>
        `;
        })
}
getPokemon();
