(async () => {
	const lockedColor = "#ccc";
	const unlockedColor = "#def";
	const selectedColor = "#33C3F0";

	let dataset = await fetch('/api/quest-graph-data/');
	let response = await dataset.json();

	let nodes = new vis.DataSet(response.nodes);
	let edges = new vis.DataSet(response.edges);  

	const container = document.getElementById("questtree");
	const data = {
		nodes: nodes,
		edges: edges
	};
	const options = {
		interaction: {
			selectConnectedEdges: false
		},
		nodes: {
			chosen: false,
			shape: "dot",
			size: 10,
			color: lockedColor,
			font: {
				face: "Raleway, Helvetica, Arial",
				size: 11,
				color: "#666"
			},
			borderWidth: 1,
		},
		edges: {
			color: lockedColor,
			dashes: true,
			arrows :{
				to:{
					scaleFactor: 0.5
				}
			}		
		},
		layout: {
			hierarchical: {
				direction: "RL"
			}
		}
	};
	let network = new vis.Network(container, data, options);
	let wallet = 30;

	/* ********************************************************************************* */
	
	/**
		update all graph nodes with selectedParents and subTree Requirements
		change visuals based on status (values / requirements / selected)
	**/
	const buildGraphDisplay = function() {
		//update wallet display
		document.getElementById("wallet2").innerHTML = wallet;


		/* recursive subTree (classic) */
		/*
		const getRSubtree = nodeId => {
			let childs = network.getConnectedNodes(nodeId, "from");
			if (childs.length > 0) {
				let subtree = childs;
				for (let i = 0; i < childs.length; i++) {
					let nodeChilds = getSubtree(childs[i]);
					if (nodeChilds) {
						subtree = subtree.concat(nodeChilds);
					}
				}
				return subtree;
			}
			return false;
		};
		*/

		/* SUBTREE */
		/* glitch subtree */
		const getSubtree = nodeId => {
			let childs = network.getConnectedNodes(nodeId, "from");
			for (let i = 0; i < childs.length; i++) {
				childs = childs.concat(network.getConnectedNodes(childs[i], "from"));
			}
			return childs;
		};

		/* glitch parentTree */
		const getParentstree = nodeId => {
			let parents = network.getConnectedNodes(nodeId, "to");
			for (let i = 0; i < parents.length; i++) {
				parents = parents.concat(network.getConnectedNodes(parents[i], "to"));
			}
			return parents;
		};

		nodes.getIds().forEach(nodeId => {
			let currNode = nodes.get(nodeId);
			
			// updating nodes with subtree
			// example using reduce
			currNode.requiredSubtree = getSubtree(nodeId).reduce( (requiredNodes, id) => { 
				const childNode = nodes.get(id);
				(childNode.selected !== true && typeof requiredNodes.find(o => o.id === childNode.id) === "undefined" && requiredNodes.push(childNode));
				return requiredNodes;
			}, []);
			
			// updating nodes with parentspath 
			// example with forEach
			let selectedParents = [];
			getParentstree(nodeId).forEach(node => {
				const parentNode = nodes.get(node);
				(parentNode.selected === true && typeof selectedParents.find(o => o.id === parentNode.id) === "undefined" && selectedParents.push(parentNode));
			});
			currNode.selectedParents = selectedParents;

			// by default mark all as available
			currNode.locked = "";
			//trigger errors for unselected nodes
			if (currNode.selected !== true){
				if (currNode.requiredSubtree.length > 0) {
					// if missing nodes in path mark as locked
					currNode.locked += "/!\\ ALERTE REQUIREMENTS /!\\ \n Pour debloquer cette compétence, il faut acquérir les compétences suivantes : \n- " + currNode.requiredSubtree.map( n => n.label.replace("\n"," ")).join("\n- ") ;
				}else if (nodes.get(nodeId).value > wallet) {
					// if not enough credit mark as locked
					currNode.locked += "/!\\ ALERTE PAUVRETÉ /!\\ \n Pas assez de crédits, il t'en reste " + wallet +"\n";
				}
			}
				
			// change node visuals
			currNode.color = {
				background: (currNode.selected === true)?selectedColor:(currNode.locked === "")?unlockedColor:lockedColor,
				highlight: {
					background: (currNode.selected === true)?selectedColor:(currNode.locked === "")?unlockedColor:lockedColor,
				},
			};
			currNode.shapeProperties = (currNode.locked === "") ? { borderDashes : false} : { borderDashes : [6,4] } ;
			currNode.refund = Math.round(currNode.selectedParents.reduce( (parentsRefund, node) => parentsRefund + node.value, currNode.value )*0.9);
			currNode.title = (currNode.selected === true)?  currNode.label +" : Compétence acquise<br/> Refund pour "+ currNode.refund +" crédits" :(currNode.locked === "")? "Acquerir "+ currNode.label +" pour "+currNode.value +" crédits" : currNode.locked.replace(/\n/g,"<br/>");
			/*
			currNode.borderWidth = (currNode.selected == true)?2:1;
			currNode.borderWidthSelected = (currNode.selected == true)?2:1;
			*/
			nodes.update(currNode);

			const connectedEdges = network.getConnectedEdges(currNode.id);
			connectedEdges.forEach(id => {
				const edge = edges.get(id);
				if(edge.to == currNode.id){
					edge.dashes = (currNode.selected === true)?false:true;
					edges.update(edge);
				}
			});
			
		});

	};

	/* EVENTS HANDLING */
	/**
		init
	**/
	network.once("stabilized", () => {
		buildGraphDisplay();
	});

	network.once('afterDrawing', function () {
		// Assuming 'container' is the DOM element where the network is rendered
		var containerWidth = container.offsetWidth;
		var containerHeight = container.offsetHeight;
		var scale = 1;
		network.moveTo({
			offset: {
				x: (0.5 * containerWidth) * scale,
				y: (0.4 * containerHeight) * scale
			},
			scale: scale
		});});
	
	/**
		on click, update graph nodes selected status, handle wallet
	**/
	network.on("click", p => {
		if (p.nodes.length) {
			let currNode = nodes.get(p.nodes[0]);
			if (currNode.locked == ""){
				if (currNode.selected == true){
					currNode.selectedParents.forEach( node => {
						node.selected = false;
						nodes.update(node);
					});
				}else{
					$('#questmodal').modal('show');
					$('#questtask').html(currNode.quest);
				}
				nodes.update(currNode);

				document.getElementById("wallet").innerHTML = wallet;
			}else{
				// No need to alert, those are displayed in tooltips
				// alert(currNode.locked);
			}
			buildGraphDisplay();
		}
	});
})();
