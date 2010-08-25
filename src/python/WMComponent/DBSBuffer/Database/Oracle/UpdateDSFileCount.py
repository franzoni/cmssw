#!/usr/bin/env python
"""
_DBSBuffer.NewFile_

Add a new file to DBS Buffer: Oracle version

"""
__revision__ = "$Id: UpdateDSFileCount.py,v 1.2 2009/06/04 21:52:14 mnorman Exp $"
__version__ = "$Revision: 1.2 $"
__author__ = "mnorman@fnal.gov"

#This has been updated for use with Oracle


from WMComponent.DBSBuffer.Database.MySQL.UpdateDSFileCount import UpdateDSFileCount as MySQLUpdateDSFileCount

class UpdateDSFileCount(MySQLUpdateDSFileCount):
	"""
	_DBSBuffer.NewFile_
	
	Add a new file to DBS Buffer: Oracle version
	
	"""


	sql = """UPDATE dbsbuffer_dataset a
	      SET UnMigratedFiles = (SELECT count(*) FROM dbsbuffer_file f
	      WHERE f.status  = 'NOTUPLOADED'
	      AND   f.dataset = a.ID
	      AND   a.Path    = :path)
	"""

#	sql = """
#UPDATE dbsbuffer_dataset a
#        SET UnMigratedFiles = (SELECT count(*) FROM dbsbuffer_file f
#	   WHERE f.status  = 'NOTUPLOADED'
#	   AND   f.dataset = a.ID
#	)
#	WHERE ID IN (SELECT ID from dbsbuffer_dataset WHERE Path=:path)
#	"""






