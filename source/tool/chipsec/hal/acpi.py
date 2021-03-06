#!/usr/local/bin/python
#CHIPSEC: Platform Security Assessment Framework
#Copyright (c) 2010-2015, Intel Corporation
# 
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; Version 2.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#Contact information:
#chipsec@intel.com
#




# -------------------------------------------------------------------------------
#
# CHIPSEC: Platform Hardware Security Assessment Framework
# (c) 2010-2012 Intel Corporation
#
# -------------------------------------------------------------------------------

"""
HAL component providing access to and decoding of ACPI tables
"""

__version__ = '0.1'

import struct
import sys

from collections import namedtuple

from chipsec.logger import *
from chipsec.file import *

import chipsec.hal.acpi_tables
import chipsec.hal.uefi

class AcpiRuntimeError (RuntimeError):
    pass

# ACPI Table Header Format
ACPI_TABLE_HEADER_FORMAT = '=4sIBB6s8sI4sI'
ACPI_TABLE_HEADER_SIZE   = struct.calcsize(ACPI_TABLE_HEADER_FORMAT) # 36
assert( 36 == ACPI_TABLE_HEADER_SIZE )

class ACPI_TABLE_HEADER( namedtuple('ACPI_TABLE_HEADER', 'Signature Length Revision Checksum OEMID OEMTableID OEMRevision CreatorID CreatorRevision') ):
    __slots__ = ()
    def __str__(self):
        return """  Table Header
------------------------------------------------------------------
  Signature        : %s
  Length           : 0x%08X
  Revision         : 0x%02X
  Checksum         : 0x%02X
  OEM ID           : %s
  OEM Table ID     : %s
  OEM Revision     : 0x%08X
  Creator ID       : %s
  Creator Revision : 0x%08X
""" % ( self.Signature, self.Length, self.Revision, self.Checksum, self.OEMID, self.OEMTableID, self.OEMRevision, self.CreatorID, self.CreatorRevision )


ACPI_TABLE_SIG_SIZE = 0x4

ACPI_TABLE_SIG_ROOT = 'ROOT' 
ACPI_TABLE_SIG_RSDP = 'RSDP'
ACPI_TABLE_SIG_RSDT = 'RSDT'
ACPI_TABLE_SIG_XSDT = 'XSDT'
ACPI_TABLE_SIG_FACP = 'FACP'
ACPI_TABLE_SIG_FACS = 'FACS'
ACPI_TABLE_SIG_DSDT = 'DSDT'
ACPI_TABLE_SIG_SSDT = 'SSDT'
ACPI_TABLE_SIG_PSDT = 'PSDT'
ACPI_TABLE_SIG_APIC = 'APIC'
ACPI_TABLE_SIG_SBST = 'SBST'
ACPI_TABLE_SIG_ECDT = 'ECDT'
ACPI_TABLE_SIG_SRAT = 'SRAT'
ACPI_TABLE_SIG_SLIC = 'SLIC'
ACPI_TABLE_SIG_SLIT = 'SLIT'
ACPI_TABLE_SIG_BOOT = 'BOOT'
ACPI_TABLE_SIG_CPEP = 'CPEP'
ACPI_TABLE_SIG_DBGP = 'DBGP'
ACPI_TABLE_SIG_ETDT = 'ETDT'
ACPI_TABLE_SIG_HPET = 'HPET'
ACPI_TABLE_SIG_MCFG = 'MCFG'
ACPI_TABLE_SIG_SPCR = 'SPCR'
ACPI_TABLE_SIG_SPMI = 'SPMI'
ACPI_TABLE_SIG_TCPA = 'TCPA'
ACPI_TABLE_SIG_WDAT = 'WDAT'
ACPI_TABLE_SIG_WDRT = 'WDRT'
ACPI_TABLE_SIG_WSPT = 'WSPT'
ACPI_TABLE_SIG_WDDT = 'WDDT'
ACPI_TABLE_SIG_ASF  = 'ASF!'
ACPI_TABLE_SIG_MSEG = 'MSEG'
ACPI_TABLE_SIG_DMAR = 'DMAR'
ACPI_TABLE_SIG_UEFI = 'UEFI'
ACPI_TABLE_SIG_FPDT = 'FPDT'
ACPI_TABLE_SIG_PCCT = 'PCCT'
ACPI_TABLE_SIG_MSDM = 'MSDM'
ACPI_TABLE_SIG_BATB = 'BATB'
ACPI_TABLE_SIG_BGRT = 'BGRT'

ACPI_TABLES = {
  ACPI_TABLE_SIG_ROOT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_RSDT: chipsec.hal.acpi_tables.RSDT,
  ACPI_TABLE_SIG_XSDT: chipsec.hal.acpi_tables.XSDT,
  ACPI_TABLE_SIG_FACP: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_FACS: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_DSDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_SSDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_PSDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_APIC: chipsec.hal.acpi_tables.APIC,
  ACPI_TABLE_SIG_SBST: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_ECDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_SRAT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_SLIC: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_SLIT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_BOOT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_CPEP: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_DBGP: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_ETDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_HPET: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_MCFG: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_SPCR: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_SPMI: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_TCPA: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_WDAT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_WDRT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_WSPT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_WDDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_ASF : chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_MSEG: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_DMAR: chipsec.hal.acpi_tables.DMAR,
  ACPI_TABLE_SIG_UEFI: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_FPDT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_PCCT: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_MSDM: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_BATB: chipsec.hal.acpi_tables.ACPI_TABLE,
  ACPI_TABLE_SIG_BGRT: chipsec.hal.acpi_tables.ACPI_TABLE
}

########################################################################################################
#
# RSDP
#
########################################################################################################

RSDP_GUID_ACPI2_0 = '8868E871-E4F1-11D3-BC22-0080C73C8881'
RSDP_GUID_ACPI1_0 = 'EB9D2D31-2D88-11D3-9A16-0090273FC14D'


ACPI_RSDP_SIG = 'RSD PTR '
# RSDP Format
ACPI_RSDP_FORMAT = '<8sB6sBI'
ACPI_RSDP_EXT_FORMAT = 'IQB3s'
ACPI_RSDP_SIZE = struct.calcsize(ACPI_RSDP_FORMAT)
ACPI_RSDP_EXT_SIZE = struct.calcsize(ACPI_RSDP_FORMAT + ACPI_RSDP_EXT_FORMAT)
assert ACPI_RSDP_EXT_SIZE == 36

class RSDP():
    __slots__ = ()
    def __init__( self, table_content ):
        if len(table_content) == ACPI_RSDP_SIZE:
          (self.Signature, self.Checksum, self.OEMID,
           self.Revision, self.RsdtAddress) = struct.unpack(ACPI_RSDP_FORMAT, table_content)
        else:
          (self.Signature, self.Checksum, self.OEMID,
           self.Revision, self.RsdtAddress, self.Length,
           self.XsdtAddress, self.ExtChecksum, self.Reserved) = struct.unpack(ACPI_RSDP_FORMAT + ACPI_RSDP_EXT_FORMAT, table_content)
    def __str__( self ):
        default = ("==================================================================\n"
                   "  Root System Description Pointer (RSDP)\n"
                   "==================================================================\n"
                   "  Signature        : %s\n"
                   "  Checksum         : 0x%02X\n"
                   "  OEM ID           : %s\n"
                   "  Revision         : 0x%02X\n"
                   "  RSDT Address     : 0x%08X\n"
                  ) % (self.Signature, self.Checksum, self.OEMID, self.Revision, self.RsdtAddress)
        if hasattr(self, "Length"):
          default += ("  Length           : 0x%08X\n"
                      "  XSDT Address     : 0x%016X\n"
                      "  Extended Checksum: 0x%02X\n"
                      "  Reserved         : %s\n"
                     ) % (self.Length, self.XsdtAddress, self.ExtChecksum, self.Reserved.encode("hex"))
        return default

    # some sanity checking on RSDP
    def is_RSDP_valid(self ):
        return (0 != self.Checksum and (0x0 == self.Revision or 0x2 == self.Revision) )


########################################################################################################
#
# ACPI HAL Component
#
########################################################################################################

class ACPI:
    def __init__( self, cs ):
        self.cs     = cs
        self.uefi   = chipsec.hal.uefi.UEFI( self.cs )
        self.tableList = {}
        self.get_ACPI_table_list()

    def read_RSDP(self, rsdp_pa):
        rsdp_buf = self.cs.mem.read_physical_mem( rsdp_pa, ACPI_RSDP_SIZE)
        rsdp = RSDP(rsdp_buf)
        if rsdp.Revision >= 0x2:
            rsdp_buf = self.cs.mem.read_physical_mem( rsdp_pa, ACPI_RSDP_EXT_SIZE)
            rsdp = RSDP(rsdp_buf)
        return rsdp

    #
    # Searches for Root System Description Pointer (RSDP) in various locations for legacy/EFI systems
    #
    def find_RSDP( self ):
        rsdp_pa  = None
        rsdp     = None
        #
        # Check RSDP in Extended BIOS Data Area first
        #
        if logger().HAL: logger().log( "[acpi] searching RSDP in EBDA.." )
        ebda_ptr_addr = 0x40E
        ebda_addr = struct.unpack('<H', self.cs.mem.read_physical_mem( ebda_ptr_addr, 2 ))[0] << 4
        if ebda_addr > 0x400 and ebda_addr < 0xA0000:
            membuf = self.cs.mem.read_physical_mem(ebda_addr, 0xA0000 - ebda_addr)
            pos = membuf.find( ACPI_RSDP_SIG )
            if -1 != pos:
                rsdp_pa = ebda_addr + pos
                rsdp = self.read_RSDP(rsdp_pa)
                if rsdp.is_RSDP_valid():
                    logger().log( "[acpi] found RSDP in EBDA at: 0x%016X" % rsdp_pa )
                else:
                    rsdp_pa = None
        else:
            #
            # Search RSDP in legacy BIOS E/F segments (0xE0000 - 0xFFFFF)
            #
            membuf = self.cs.mem.read_physical_mem( 0xE0000, 0x20000 )
            pos = membuf.find( ACPI_RSDP_SIG )
            if -1 != pos:
                rsdp_pa  = 0xE0000 + pos
                rsdp     = self.read_RSDP(rsdp_pa)
                if rsdp.is_RSDP_valid():
                    logger().log( "[acpi] found RSDP in BIOS E/F segments: 0x%016X" % rsdp_pa )
                else:
                    rsdp_pa = None
            else:
                #
                # Search for RSDP in the EFI memory (EFI Configuration Table)
                #
                if logger().HAL: logger().log( '[acpi] searching RSDP pointers in EFI Configuration Table..' )
                (isFound,ect_pa,ect,ect_buf) = self.uefi.find_EFI_Configuration_Table()
                if isFound:
                    if RSDP_GUID_ACPI2_0 in ect.VendorTables:
                        rsdp_pa = ect.VendorTables[ RSDP_GUID_ACPI2_0 ]
                        logger().log( '[acpi] ACPI 2.0+ RSDP {%s} in EFI Config Table: 0x%016X' % (RSDP_GUID_ACPI2_0,rsdp_pa) )
                    elif RSDP_GUID_ACPI1_0 in ect.VendorTables:
                        rsdp_pa = ect.VendorTables[ RSDP_GUID_ACPI1_0 ]
                        logger().log( '[acpi] ACPI 1.0 RSDP {%s} in EFI Config Table: 0x%016X' % (RSDP_GUID_ACPI1_0,rsdp_pa) )

                    rsdp     = self.read_RSDP(rsdp_pa)
                    if rsdp.is_RSDP_valid():
                        logger().log( "[acpi] found RSDP in EFI Config Table: 0x%016X" % rsdp_pa )
                    else:
                        rsdp_pa = None

        if rsdp_pa is not None and rsdp is not None:
            logger().log( rsdp )
            return (rsdp_pa, rsdp)

        if logger().HAL: logger().log( "[acpi] searching all EFI memory for RSDP (this may take a minute).." )
        CHUNK_SZ = 1024*1024 # 1MB
        (smram_base, smram_limit, smram_size) = self.cs.cpu.get_SMRAM()
        pa = smram_base - CHUNK_SZ
        while pa > CHUNK_SZ:
            membuf = self.cs.mem.read_physical_mem( pa, CHUNK_SZ )
            pos = membuf.find( ACPI_RSDP_SIG )
            if -1 != pos:
                rsdp_pa  = pa + pos
                if logger().VERBOSE: logger().log( "[acpi] found '%s' signature at 0x%016X. Checking if valid RSDP.." % (ACPI_RSDP_SIG,rsdp_pa) )
                rsdp     = self.read_RSDP(rsdp_pa)
                if rsdp.is_RSDP_valid():
                    logger().log( "[acpi] found RSDP in EFI memory: 0x%016X" % rsdp_pa )
                    break
            pa -= CHUNK_SZ

        if rsdp_pa is not None: logger().log( rsdp )
        return (rsdp_pa, rsdp)
    #
    # Retrieves System Description Table (RSDT or XSDT) either from RSDP or using OS API
    #
    def get_SDT( self, search_rsdp=True ):
        if search_rsdp:
            (rsdp_pa, rsdp) = self.find_RSDP()
            if 0x0 == rsdp.Revision:
                sdt_pa = rsdp.RsdtAddress
                is_xsdt = False
            elif 0x2 == rsdp.Revision:
                sdt_pa = rsdp.XsdtAddress
                is_xsdt = True
            else:
                return (False,None,None,None)
            logger().log( "[acpi] found %s at PA: 0x%016X" % ('XSDT' if is_xsdt else 'RSDT', sdt_pa) )
            sdt_header_buf = self.cs.mem.read_physical_mem( sdt_pa, ACPI_TABLE_HEADER_SIZE )
            sdt_header     = self._parse_table_header( sdt_header_buf )
            sdt_buf        = self.cs.mem.read_physical_mem( sdt_pa, sdt_header.Length )
        else:
            logger().log( "[acpi] reading RSDT/XSDT using OS API.." )
            (sdt_buf, is_xsdt) = self.cs.helper.get_ACPI_SDT()
            sdt_header = self._parse_table_header( sdt_buf[ :ACPI_TABLE_HEADER_SIZE] )

        sdt_contents = sdt_buf[ ACPI_TABLE_HEADER_SIZE : ]
        sdt = ACPI_TABLES[ACPI_TABLE_SIG_XSDT if is_xsdt else ACPI_TABLE_SIG_RSDT]()
        sdt.parse( sdt_contents )
        return (is_xsdt,sdt_pa,sdt,sdt_header)


    #
    # Populates a list of ACPI tables available on the system
    #
    def get_ACPI_table_list( self ):
        addresses = []
        # find RSDT/XSDT table
        (is_xsdt,sdt_pa,sdt,sdt_header) = self.get_SDT()

        # cache RSDT/XSDT in the list of ACPI tables
        if sdt_pa is not None: self.tableList[ sdt_header.Signature ] = sdt_pa

        # cache other ACPI tables in the list
        for a in sdt.Entries:
            _sig = self.cs.mem.read_physical_mem( a, ACPI_TABLE_SIG_SIZE )
            if _sig not in ACPI_TABLES.keys():
                logger().warn( 'Unknown ACPI table signature: %s' % _sig )
            self.tableList[ _sig ] = a

        return self.tableList

    #
    # Checks is ACPI table with <name> is available on the system
    #
    def is_ACPI_table_present( self, name ):
        return (name in self.tableList)

    #
    # Prints a list of ACPI tables available on the system
    #
    def print_ACPI_table_list(self):
        if len( self.tableList ) == 0:
            logger().error("Couldn't get list of ACPI tables")
        else:
            if logger().HAL: logger().log( "[acpi] Found the following ACPI tables:" )
            for tableName in sorted(self.tableList.keys()):
                logger().log( " - %s: 0x%016X" % (tableName,self.tableList[tableName]) )

    #
    # Retrieves contents of ACPI table from memory or from file
    #
    def get_parse_ACPI_table( self, name, isfile = False ):
        (table_header_blob,table_blob)=self.get_ACPI_table(name,isfile)
        if table_header_blob is not None:
            return self._parse_table( name, table_header_blob, table_blob )
        
    def get_ACPI_table( self, name, isfile = False ):
        table_header_blob  = None
        table_blob = None
        t_data = None
        if isfile == True:
            t_data = chipsec.file.read_file( name )
        else:
            t_size = self.cs.mem.read_physical_mem_dword( self.tableList[name] + 4 )
            t_data = self.cs.mem.read_physical_mem( self.tableList[name], t_size )

        if t_data is not None:
            table_header_blob  = t_data[ : ACPI_TABLE_HEADER_SIZE ]
            table_blob         = t_data[ ACPI_TABLE_HEADER_SIZE : ]

        return (table_header_blob,table_blob)
    
    #
    # Dumps contents of ACPI table
    #
    def dump_ACPI_table( self, name, isfile = False ):
        (table_header,table,table_header_blob,table_blob) = self.get_parse_ACPI_table( name, isfile )
        logger().log( "==================================================================" )
        logger().log( "ACPI Table: %s" % name )
        logger().log( "==================================================================" )
        # print table header
        logger().log( table_header )
        print_buffer( table_header_blob )
        # print table contents
        logger().log( '' )
        logger().log( table )
        print_buffer( table_blob )
        logger().log( '' )

    # --------------------------------------------------------------------
    # Internal ACPI table parsing functions
    # --------------------------------------------------------------------

    def _parse_table( self, name, table_header_blob, table_blob ):
        table_header       = self._parse_table_header( table_header_blob )
        table              = self._parse_table_contents( name, table_blob )
        return (table_header,table,table_header_blob,table_blob)


    def _parse_table_header( self, header ):
        acpi_table_hdr = ACPI_TABLE_HEADER( *struct.unpack_from( ACPI_TABLE_HEADER_FORMAT, header ) )
        if logger().VERBOSE: logger().log( acpi_table_hdr ) 
        return acpi_table_hdr


    def _parse_table_contents( self, signature, contents ):
        table = None
        if ACPI_TABLES.__contains__(signature):
            table = (ACPI_TABLES[signature])() 
            table.parse( contents )
        return table

