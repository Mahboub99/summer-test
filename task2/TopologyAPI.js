const fs = require('fs');
const path = require('path');
const promisify = require('util').promisify;

const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);

/**
 * Topology API library class
 * 
 * @author Ahmed Mahboub
 * @class ToplogyAPI
 */
class TopologyAPI {
    /**
     * TopologyAPI class constuctor
     * @constructor 
     * @author Ahmed Mahboub
     * @returns {void}
     */
    constructor() {
        /**
         * stor topologies in memory
         * @author Ahmed Mahboub
         * @type Array
         */
        this.topologies = []
    }

    /**
     * Get topology by ID
     * @author Ahmed Mahboub
     * @param {String} id 
     * @returns {Object}
     */
    getTopology(id) {
        const result = this.topologies.filter(topology => topology.id === id);

        if (result.length == 0)
            return null;

        return result[0];
    }

    /**
     * return all topologies in memory
     * @author Ahmed Mahboub
     * @returns {Array<Object>}
     */
    async queryTopologies() {
        return this.topologies;
    }

    /**
     * Read Json from disk
     * @author Ahmed Mahboub
     * @param {String} fileName 
     * @returns {Object}
     */
    async readJson(fileName) {
        const data = await readFile(path.resolve() + `/${fileName}.json`);
        const topology = JSON.parse(data);

        this.topologies.push(topology);

        return topology;
    }

    /**
     * Write Json to disk
     * @author Ahmed Mahboub
     * @param {String} id 
     * @returns {Object}
     */
    async writeJson(id) {
            const topology = this.getTopology(id);

            if (!topology) {
                return null;
            }

            await writeFile(path.resolve() + `/output/topology_${id}.json`, JSON.stringify(topology));

            return topology;
        }
        /**
         * Delete topology from memory
         * @author Ahmed Mahboub
         * @param {String} id 
         * @returns {Object}
         */
    async deleteTopology(id) {
        const deletedTopology = this.getTopology(id);

        if (!deletedTopology) {
            return null;
        }

        this.topologies = this.topologies.filter(topology => topology.id !== id);
        return deletedTopology;
    }

    /**
     * return all devices of a topology with the given id
     * @author Ahmed Mahboub
     * @param {String} id 
     * @returns {Array<Object>}
     */
    async queryDevices(id) {
        const topology = this.getTopology(id);

        if (!topology) {
            return null;
        }

        const { components } = topology;
        return components;
    }

    /**
     * return all devices of a topology with the given id and netlistNodeID
     * @author Ahmed Mahboub
     * @param {String} id 
     * @param {String} netlistNodeID 
     * @returns {Array<Object>}
     */
    async queryDevicesWithNetlistNode(id, netlistNodeID) {
        const topology = this.getTopology(id);

        if (!topology) {
            return null;
        }

        const { components } = topology;

        const result = [];

        components.forEach(component => {

            for (const netlistNode of Object.values(component.netlist)) {
                if (netlistNode === netlistNodeID) {
                    result.push(component);
                    break;
                }
            }
        });

        return result;
    }
}

async function test() {
    const obj = new TopologyAPI();

    await obj.readJson('topology');
    await obj.queryTopologies();
    await obj.deleteTopology("top1");
}

test();


module.exports = TopologyAPI;