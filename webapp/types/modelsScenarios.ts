type LcsType = 'dynamic' | 'static'

export const lcs: Record<lcsType, string> = {
  dynamic: 'Dynamic',
  static: 'Static',
}

type Model =
  | 'ACCESS1-0'
  | 'BCC-CSM1-1'
  | 'BNU-ESM'
  | 'CCSM4'
  | 'GFDL-ESM2G'
  | 'GFDL-ESM2M'
  | 'IPSL-CM5A-LR'
  | 'IPSL-CM5A-MR'
  | 'MIROC5'
  | 'MIROC-ESM'
  | 'MIROC-ESM-CHEM'
  | 'MRI-CGCM3'
  | 'NorESM1-M'

export const models: Record<Model, string> = {
  'ACCESS1-0': 'ACCESS1-0', // does not have RCP 2.6 or 6.0
  'BCC-CSM1-1': 'BCC-CSM1-1',
  'BNU-ESM': 'BNU-ESM', // does not have RCP 2.6 or 6.0
  CCSM4: 'CCSM4',
  'GFDL-ESM2G': 'GFDL-ESM2G',
  'GFDL-ESM2M': 'GFDL-ESM2M',
  'IPSL-CM5A-LR': 'IPSL-CM5A-LR',
  'IPSL-CM5A-MR': 'IPSL-CM5A-MR',
  MIROC5: 'MIROC5',
  'MIROC-ESM': 'MIROC-ESM',
  'MIROC-ESM-CHEM': 'MIROC-ESM-CHEM',
  'MRI-CGCM3': 'MRI-CGCM3',
  'NorESM1-M': 'NorESM1-M',
}

type Scenario = 'rcp45' | 'rcp60' | 'rcp85'

export const scenarios: Record<Scenario, string> = {
  rcp45: 'RCP 4.5',
  rcp60: 'RCP 6.0',
  rcp85: 'RCP 8.5',
}

type Era = '2016-2045' | '2046-2075' | '2071-2100'

export const eras: Record<Era, string> = {
  '2016-2045': '2016-2045',
  '2046-2075': '2046-2075',
  '2071-2100': '2071-2100',
}
