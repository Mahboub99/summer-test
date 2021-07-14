const TopologyAPI = require('./');

describe('TopologyAPI test', () => {
    let topologyAPI;

    beforeEach(async() => {
        topologyAPI = new TopologyAPI();
        await topologyAPI.readJson('topology');
        await topologyAPI.readJson('topology1');
        await topologyAPI.readJson('topology2');
        await topologyAPI.readJson('topology3');

    });

    describe('readJson', () => {
        it('should be length 4', () => {
            expect(topologyAPI.topologies.length).toBe(4);
        })
    })

    describe('queryTopologies', () => {
        it('should return all topologies', async() => {
            const result = await topologyAPI.queryTopologies();
            expect(result).toMatchObject(topologyAPI.topologies);
        })
    })

    describe('deleteTopology', () => {
        it('should reduce length by one', async() => {
            await topologyAPI.deleteTopology("top1");
            expect(topologyAPI.topologies.length).toBe(3);
        })

        it('should return deleted topology', async() => {
            const result = await topologyAPI.deleteTopology("top1");
            expect(result.id).toBe("top1");
        })
    })

    describe('queryDevices', () => {
        it('should return topologies components', async() => {
            const result = await topologyAPI.queryDevices("top1");
            expect(result).toMatchObject(topologyAPI.topologies[0].components);
        })
    })

    describe('queryDevicesWithNetlistNode', () => {
        it('should return topologies components that connected to a given node', async() => {
            const result = await topologyAPI.queryDevicesWithNetlistNode("top1", "vss");
            expect(result).toMatchObject([topologyAPI.topologies[0].components[1]]);
        })
    })
});