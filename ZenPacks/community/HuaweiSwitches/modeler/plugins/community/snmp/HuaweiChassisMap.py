from Products.DataCollector.plugins.CollectorPlugin import (SnmpPlugin, GetTableMap, GetMap) 
from Products.DataCollector.plugins.DataMaps import (ObjectMap, RelationshipMap, MultiArgs)

class HuaweiChassisMap(SnmpPlugin): 
    """ Models Huawei chassis switches for components  """
    snmpGetTableMaps = (
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
        """Process SNMP data and return a relationship map"""
        log.info('processing %s for device %s', self.name(), device.id)
        
        maps = []
        mpumap = []
        lpumap = []      
   
        getdata, tabledata = results
  
        hwinfo = tabledata.get('entPhysicalTable', {})
       
        for snmpindex, hwrow in hwinfo.items():
            entname = hwrow.get('entPhysicalName')
    
            if entname.startswith("MPU Board"):
                name = 'Slot ' + str(entname.split()[-1])

                mpumap.append(ObjectMap({
                    'id': self.prepId(name),
                    'title': name,
                    'snmpindex': snmpindex,
                    'cardmodel':  hwrow.get('entPhysicalHardwareRev'),
                    'cardserial' : hwrow.get('entPhysicalSerialNum'),
                    'cardtype': hwrow.get('entPhysicalDescr'),
                    }))

            if entname.startswith("LPU Board"):
                name = 'Slot ' + str(entname.split()[-1])

                lpumap.append(ObjectMap({
                    'id': self.prepId(name),
                    'title': name,
                    'snmpindex': snmpindex,
                    'cardmodel':  hwrow.get('entPhysicalHardwareRev'),
                    'cardserial' : hwrow.get('entPhysicalSerialNum'),
                    'cardtype': hwrow.get('entPhysicalDescr'),
                    }))


            maps.append(RelationshipMap(
                relname = 'huaweiMPUs',
                modname = 'ZenPacks.community.HuaweiSwitches.HuaweiMPU',
                objmaps = mpumap))

            maps.append(RelationshipMap(
                relname = 'huaweiLPUs',
                modname = 'ZenPacks.community.HuaweiSwitches.HuaweiLPU',
                objmaps = lpumap))

        return maps
