# have to change period 1 & period 2
import datetime
end = int(datetime.datetime.combine(datetime.datetime.today(), datetime.time(0, 0, 0, 0)).timestamp())
start = int(datetime.datetime(2015, 1, 22).timestamp())


all_stocks_info = [{
    "name": "AEX", 
    "symbol": "%5EAEX",
    "start": start,
    "end": end
}, {
    "name": "ATX",
    "symbol": "%5EATX",
    "start": start,
    "end": end
}, {
    "name":"BEL_20", 
    "symbol":"%5EBFX",
    "start": start,
    "end": end
}, {
    "name": "BIST_100",
    "symbol":"XU100.IS",
    "start": start,
    "end": end
}, { 
    "name": "Bovespa", 
    "symbol":"%5EBVSP",
    "start": start,
    "end": end
}, {
    "name": "BSE_Sensex", 
    "symbol": "%5EBSESN",
    "start": start,
    "end": end
# }, {
#     "name": "Budapest_SE", 
#     "symbol": "^BUX.BD",
#    "domain": ''
}, {
    "name": "CAC40",
    "symbol": "%5EFCHI",
    "start": start,
    "end": end
#}, {
#    "name": "China_A50",
#    "symbol": "XIN9.FGI",
#    "domain": ""
# }, {
#     "name": "COLCAP",
#     "symbol": "%5ESPCOSLCP",
#    "start": start,
#    "end": end
}, {
    "name": "CSE", 
    "symbol": "%5EGSPTSE",
    "start": start,
    "end": end
}, {
    "name": "DAX_PERFORMANCE-INDEX", 
    "symbol": "%5EGDAXI",
    "start": start,
    "end": end
}, {
    "name": "Dow_30",
    "symbol": "%5EDJI",
    "start": start,
    "end": end
}, {
    "name":"Euro_Stoxx_50",
    "symbol": "SX5E.SW", 
    "start": start,
    "end": end
}, {
    "name":"EURONEXT_100",
    "symbol": "%5EN100",
    "start": start,
    "end": end
# }, {
#     "name":"FTSE_100",
#     "symbol": "%5EFTSE", 
#     "domain": 
# }, {
#     "name": "FTSE_MIB",
#    "symbol": "FTSEMIB.MI",
#     "domain": ""
# }, {
#     "name":"FTSE_Bursa_Malaysia_KLCI",
#    "symbol": "%5EKLSE",
#    "start": start,
#    "end": end
}, {
    "name":"HANG_SENG_INDEX",
    "symbol": "%5EHSI", 
    "start": start,
    "end": end
}, {
#     "name": "HNX_30",
#   "symbol": "???",
#    "domain": ""
#}, {
    "name": "IBEX_35",
    "symbol": "%5EIBEX",
    "start": start,
    "end": end
}, {
    "name": "IDX_Composite",
    "symbol": "%5EJKSE",
    "start": start,
    "end": end
}, {
    "name":"KOSPI_Composite_Index",
    "symbol": "%5EKS11",
    "start": start,
    "end": end
}, {
    "name":"MOEX_Russia_Index",
    "symbol": "IMOEX.ME",
    "start": start,
    "end": end
}, {
    "name":"Nasdaq",
    "symbol": "%5EIXIC",
    "start": start,
    "end": end
}, {
    "name":"Nifty_50",
    "symbol": "%5ENSEI",
    "start": start,
    "end": end
}, {
    "name":"IPC_MEXICO",
    "symbol": "%5EMXX",
    "start": start,
    "end": end
}, {
    "name":"MERVAL",
    "symbol": "%5EMERV",
    "start": start,
    "end": end
}, {
    "name":"Nikkei_225",
    "symbol": "%5EN225",
    "start": start,
    "end": end
}, {
    "name":"Russell_2000",
    "symbol": "%5ERUT",
    "start": start,
    "end": end
}, {
    "name":"SP_500",
    "symbol": "%5EGSPC", 
    "start": start,
    "end": end
# }, {
#    "name":"SP_CLX",
#    "symbol": "%5EIPSA",
#    "start": start,
#    "end": end
# }, {
#     "name":"SP_Lima",
#     "symbol": "???"
#     "domain": ""
# }, {
#     "name":"SP_ASX_200",
#     "symbol": "???",
#     "domain": ""
# }, {
#     "name":"SP_CLX_IPSA",
#     "symbol": "SP-IPSA.SN",
#     "domain": ""
}, {
    "name":"SP_NZX_50_INDEX_GROSS",
    "symbol": "%5ENZ50",
    "start": start,
    "end": end
}, {
    "name":"SP_TSX_Composite_index",
    "symbol": "%5EGSPTSE", 
    "start": start,
    "end": end
}, {
    "name": "SMI",
    "symbol": "%5ESSMI",
    "start": start,
    "end": end
},{
    "name": "SSE",
    "symbol": "%5ESSEC",
    "start": start,
    "end": end
}, {
    "name": "TA_35",
    "symbol": "TA35.TA",
    "start": start,
    "end": end
#}, {
#    "name":"Tadawul",
#    "symbol": "^TASI.SR",
#    "domain": ""
}, {
    "name": "Taiwan_Weighted",
    "symbol": "%5ETWII",
    "start": start,
    "end": end
#}, {
#    "name": "WIG20",
#    "symbol": "PLX.DE",
#    "domain": ""
}]
