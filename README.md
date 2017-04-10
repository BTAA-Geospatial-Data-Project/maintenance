# maintenance

JSONmetadata_comparison.py checks Esri Open Data Portals for new, modified, or deleted resources. To run this scripts, you should have a directory containing two folders - 'Jsons' and 'Reports' - and a 'PortalList.csv' with two columns (portalName and URL) describing data portals to be checked for changed records.  You also will need to manually edit a few items in a section near the beginning of the script  1) PreviousActionDate and ActionDate (in YYYYMMDD format)
2) directory path (containing the portal list csv and folders "Jsons" and "Reports")
3) a list of fields desired in the printed report

SocrataJSON_metadata_comparison.py is very similar to the script above but altered for use on Socrata data portals.  The requirements for running the script are the same but the CSV should be named 'SocrataPortalList.csv'
