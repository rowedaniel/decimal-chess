
const socket = io();


let lastSelectedTile;
let selectingTile = false;

let get_tile = function(row, col)
{
    row = 8-row;
    col += 1;
    return document.querySelector(`tr:nth-child(${row}) td:nth-child(${col})`);
}
let get_tile_loc = function(tile)
{
    let row = -1;
    let col = -1;
    do_on_all_tiles(function(r,c, t) {
        if(t === tile) {
            row = r;
            col = c;
        }
    });
    return [row, col, 0];
}

let get_piece = function(row, col, index)
{
    // TODO: fix later
    let tile = get_tile(row, col);
    if(!tile) {
        return tile;
    }
    index += 1;
    return tile.querySelector(`div:nth-child(${index})`);
}
let get_piece_loc = function(tile)
{
    let row = -1;
    let col = -1;
    let index = -1;
    do_on_all_pieces(function(r,c,i, t) {
        if(t === tile) {
            row = r;
            col = c;
            index = i;
        }
    });
    return [row, col, index];
}

let do_on_all_tiles = function(func)
{
    for(let row = 0; row < 8; ++row) {
        for(let col = 0; col < 8; ++col) {
            let i=0;
            let tile = get_tile(row, col);
            if(tile) {
                func(row, col, tile);
            }
        }
    }
}
let do_on_all_pieces = function(func)
{
    do_on_all_tiles(function(r,c,tile){
        let i =0;
        let piece = get_piece(r,c,0);
        while(piece) {
            func(r,c,i, piece);
            piece = get_piece(r,c,++i);
        }

    });
}

let wipe_tiles = function() {
    do_on_all_tiles(function(row, col, tile) {
        tile.className = "";
        while(tile.firstChild) {
            tile.removeChild(tile.firstChild);
        }
    });
}
let clear_tile_movable = function()
{
    do_on_all_tiles(function(row, col, tile) {
        tile.classList.remove("movable");
    });
}
let clear_tile_selected = function(event)
{
    do_on_all_tiles(function(row, col, tile) {
        tile.classList.remove("move-to");
        tile.classList.remove("selected");
    });
}


let select_piece = function(piece, tile)
{
    clear_tile_selected();
    if(selectingTile) {
        selectingTile = false;
        let [r1,c1,i1] = lastSelectedTile;
        let [r2,c2,i2] = get_piece_loc(piece);
        console.log("moving!", r1,c1,i1, r2,c2,i2);
        socket.emit("q_move", {
           "from" : {"row" : r1, "col" : c1, "index" : i1}, 
           "to"   : {"row" : r2, "col" : c2, "index" : i2} 
        });
    }

    else {
        lastSelectedTile = get_piece_loc(piece);
        selectingTile = true;

        tile.classList.add("selected");
        do_on_all_tiles(function(row, col, tile) {
            if(tile.classList.contains("movable")) {
                console.log("adding class");
                tile.classList.remove("movable");
                tile.classList.add("move-to");
            }
        });
    }
}

let select_tile = function(tile) {
    if(!selectingTile || tile.firstChild) {
        return;
    }

    clear_tile_selected();
    selectingTile = false;
    let [r1,c1,i1] = lastSelectedTile;
    let [r2,c2,i2] = get_tile_loc(tile);
    console.log("moving!", r1,c1,i1, r2,c2,i2);
    socket.emit("q_move", {
       "from" : {"row" : r1, "col" : c1, "index" : i1}, 
       "to"   : {"row" : r2, "col" : c2, "index" : i2} 
    });
}



window.addEventListener("DOMContentLoaded", function(event) {


    socket.on("r_update_pieces", function(data) {
        wipe_tiles();
        for(let key in data["pieces"]) {
            let keyparts = key.split(',');
            let row = parseInt(keyparts[0]);
            let col = parseInt(keyparts[1]);

            let tile = get_tile(row, col);
            if(!tile) { continue; }

            let piece = document.createElement("div");
            piece.addEventListener("mouseover", function(event) {
                let [row,col,index] = get_piece_loc(piece);
                socket.emit('q_view', {'row': row, 'col': col, 'index':index});
            });
            piece.addEventListener("click", function(event) {
                select_piece(piece, tile);
            });
            for(let c of data["pieces"][key]) {
                piece.classList.add(c);
            }
            tile.appendChild(piece);

            // update all other pieces in tile so you can see all of them
            const n = tile.children.length
            for(let i=0; i<n; ++i) {
                tile.children[i].style.left = 100*(i/n) + "%";
                tile.children[i].style.width = 100*(1/n) + "%";
            }
        }
        if("color" in data) {
            document.getElementById("turn-label").innerHTML = data["color"];
        }
    });



    socket.on("r_view", function(data) {
        clear_tile_movable();
        for(let loc of data) {
            let tile = get_tile(loc[0], loc[1]);
            if(!tile) {
                console.log("tile doesn't exist at:");
                console.log(loc);
            }
            tile.classList.add("movable");
        }
    });

    do_on_all_tiles(function(r,c, tile) {
        tile.addEventListener("click", function(data) {
            select_tile(tile);
        });
    });


    document.getElementById("quit-button").addEventListener("click", function() {
        socket.emit("q_quit", {});
    });

});

