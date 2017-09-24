## **getErrorMsg**

>Returns the standard human readable error message corresponding to given errorNumber.
```
	 std::string getErrorMsg(const int errorNumber)
	
```
### PARAMETERS:
| NAME | TYPE | DESCRIPTION |
|------ | ------ | -------------|
|errorNumber|int|Error number whose string to return.|

### RETURN VALUE:
|TYPE | DESCRIPTION |
|------|-------------|
|string|Standard error string corresponding to given errorNumber.|

___
## **construct**

>Fills the given AddrIPv4 structure object with given ip address and port.
```
	 int construct(AddrIPv4 &_addrStruct, const char _addr[],
	                     const int _port) noexcept
	
```
### PARAMETERS:
| NAME | TYPE | DESCRIPTION |
|------ | ------ | -------------|
|_addrStruct|AddrIPv4|Ipv4 structure object that needs to be filled with given ip address and port.|
|_addr|char []|Ip address which needs to be filled in the AddrIPv4 structure object.|
|_port|int|Port number which needs to be filled in the AddrIPv4 structure object.|

### RETURN VALUE:
|TYPE | DESCRIPTION |
|------|-------------|
|int|1 if sucessful, 0 if given ip address does not represent a valid ip address, -1 if some error occurred.|

___
## **construct**

>Fills the given AddrIPv6 structure object with given ip address and port.
```
	 int construct(AddrIPv6 &_addrStruct, const char _addr[],
	                     const int _port) noexcept
	
```
### PARAMETERS:
| NAME | TYPE | DESCRIPTION |
|------ | ------ | -------------|
|_addrStruct|AddrIPv6|- Ipv6 structure object that needs to be filled with given ip address and port.|
|_addr|char []|Ip address which needs to be filled in the AddrIPv6 structure object.|
|_port|int|Port number which needs to be filled in the AddrIPv6 structure object.|

### RETURN VALUE:
|TYPE | DESCRIPTION |
|------|-------------|
|int|1 if sucessful, 0 if given ip address does not represent a valid ip address, -1 if some error occurred.|

___
## **construct**

>Fills the given AddrUnix structure object with given address.
```
	 int construct(AddrUnix &_addrStruct, const char _addr[]) noexcept
	
```
### PARAMETERS:
| NAME | TYPE | DESCRIPTION |
|------ | ------ | -------------|
|_addrStruct|AddrUnix|structure object that needs to be filled with given path.|
|_addr|char []|Path which needs to be filled in the AddrUnix structure object.|

### RETURN VALUE:
|TYPE | DESCRIPTION |
|------|-------------|
|int|Always returns 1.|

___
