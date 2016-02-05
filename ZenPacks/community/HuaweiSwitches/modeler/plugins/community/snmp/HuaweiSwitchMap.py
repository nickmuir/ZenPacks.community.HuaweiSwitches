"""Models Huawei switches for Serial number and software version, stack wise"""
from Products.DataCollector.plugins.CollectorPlugin import (SnmpPlugin, GetMap) 
from Products.DataCollector.plugins.DataMaps import ObjectMap, MultiArgs


class HuaweiSwitchMap(SnmpPlugin):
    """Retieves SNMP data then processes it"""


    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.2011.5.25.183.1.5.0':'hwStackIsStackDevice',
        '.1.3.6.1.2.1.47.1.1.1.1.10.67108867':'entPhysicalSoftwareRev',
        '.1.3.6.1.2.1.47.1.1.1.1.11.67108867':'entPhysicalSerialNum',

    })

    def process(self, device, results, log): 
        """Processes snmp data and returns map"""
        log.info('processing %s for device %s', self.name(), device.id)
        
        maps = []
        getdata, tabledata = results
  
        stack = getdata.get('hwStackIsStackDevice')

        switchserial = getdata.get('entPhysicalSerialNum')
        softwareversion = getdata.get('entPhysicalSoftwareRev')
 
        # Map main device details

        if stack == 1:
            switchserial = "N/A"
 
        maps.append(ObjectMap(
            modname = 'ZenPacks.community.HuaweiSwitches.HuaweiSwitchDevice',
            data = {
                'setHWSerialNumber': switchserial,
                'setOSProductKey': MultiArgs(softwareversion.split()[-1], 'HUAWEI Technology Co.,Ltd'),
            }))

        return maps
