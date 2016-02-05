from Products.DataCollector.plugins.CollectorPlugin import (SnmpPlugin, GetTableMap, GetMap) 
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap, MultiArgs

stackroles = {
    1 : 'master',
    2 : 'standby',
    3 : 'slave',
}


class HuaweiStackMap(SnmpPlugin): 

    snmpGetTableMaps = (
        GetTableMap( 
            'hwStackMemberInfoTable', '1.3.6.1.4.1.2011.5.25.183.1.20.1', { 
                '.2':'hwMemberStackPriority', 
                '.3':'hwMemberStackRole', 
                '.4':'hwMemberStackMacAddress',
                '.5':'hwMemberStackDeviceType',
                '.6':'hwMemberConfigStackId',
                } 
            ), 

        GetTableMap(
            'entPhysicalTable', '.1.3.6.1.2.1.47.1.1.1.1', {
                '.2':'entPhysicalDescr', 
                '.4':'entPhysicalContainedIn',
                '.7':'entPhysicalName',
                '.8':'entPhysicalHardwareRev',
                '.10':'entPhysicalSoftwareRev',
                '.11':'entPhysicalSerialNum',
                }
            ),
        )
    
    def process(self, device, results, log): 

        log.info('processing %s for device %s', self.name(), device.id)
        
        maps = []
        membermap = []
        getdata, tabledata = results;
  

        stackmembers = tabledata.get('hwStackMemberInfoTable', {}) 
        hwinfo = tabledata.get('entPhysicalTable', {})
        
       
        serials = {}    
        entid = {}

        for entindex, hwrow in hwinfo.items():
            entname = hwrow.get('entPhysicalName')
    
            if entname.startswith("MPU Board"):
                slot = entname.split()[-1]
                serials[slot] = hwrow.get('entPhysicalSerialNum') 
                entid[slot] = entindex.strip('.')

         #  Stack Members
        for snmpindex, row in stackmembers.items(): 
            name = 'Slot ' + str(row.get('hwMemberConfigStackId')) 

            if not name: 
                log.warn('Skipping switch with no id') 
                continue
 
            membermap.append(ObjectMap({ 
                'id': self.prepId(name), 
                'title': name, 
                'snmpindex': entid[str(row.get('hwMemberConfigStackId'))], 
                'stackpriority': row.get('hwMemberStackPriority'),
                'stackrole' :  stackroles.get(row.get('hwMemberStackRole'), 'unknown'), 
                'stackmac': row.get('hwMemberStackMacAddress'),
                'stackmodel': row.get('hwMemberStackDeviceType'),
                'stackserial' : serials[snmpindex.strip('.')]  
                })) 

        maps.append(RelationshipMap(
            relname = 'huaweiStackMembers',
            modname = 'ZenPacks.community.HuaweiSwitches.HuaweiStackMember',
            objmaps = membermap))
 

        return maps
