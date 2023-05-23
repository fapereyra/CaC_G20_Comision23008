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
                <p>Peso: ${data.weight} - Altura: ${data.height}</p>
            </div>
            <div class="experiencia">
                <p1>Este pokemon tiene ${data.base_experience} puntos de experiencia.<br>
                Aprovechamos para avisarte que desde Wollff creeamos que nadie nace sabiendo,<br>
                y necesario tener experiencia para poder mejorar la práctica de cualquier deporte.</p1>
            </div>
            <div class="habilidades">
                <p2>${data.abilities[0].ability.name}</p2>
                <br>
                <p2>${data.abilities[1].ability.name}</p2>
            </div>
        `;
        })
}
getPokemon();