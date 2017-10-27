#!/usr/bin/env python

from pygrap import NodeInfo, node_t

try:
    from idaapi import is_code, get_flags, get_entry_ordinal, get_entry, print_insn_mnem, generate_disasm_line
    from idc import print_operand
except:
    from idaapi import isCode
    from idc import BeginEA, GetDisasm, GetFlags, GetMnem, GetOpnd
from idagrap.error.Exceptions import CodeException


class Node(node_t):
    """Representation of a pygrap node, with useful methods.

    Args:
        ea (ea_t): Effective Address of the node.

    Attributs:
        node (node_t): Pygrap structure for a node.

    Raises:
        CodeException: If the ``ea`` is not a code instruction.
    """

    def __init__(self, ea):
        """Initialization function."""
        # Init the node structure
        node_t.__init__(self)

        # Check if it's a code instruction
        try:
            is_c = is_code(get_flags(ea))
        except:
            is_c = isCode(GetFlags(ea))
        if not is_c:
            raise CodeException

        #
        # fill node_t struct
        #

        # NodeInfo
        self.info = NodeInfo()
        inst_elements = []

        # Parse opcode and arguments        
        try:
            self.info.opcode = print_insn_mnem(ea)
        except:
            self.info.opcode = GetMnem(ea)

        nargs = 0
        
        try:
            self.info.arg1 = print_operand(ea, 0)
        except:
            self.info.arg1 = GetOpnd(ea, 0)
        if self.info.arg1 != "":
            inst_elements.append(self.info.arg1)
            nargs += 1
        try:
            self.info.arg2 = print_operand(ea, 1)
        except:
            self.info.arg2 = GetOpnd(ea, 1)
        if self.info.arg2 != "":
            inst_elements.append(self.info.arg2)
            nargs += 1
        try:
            self.info.arg3 = print_operand(ea, 2)
        except:
            self.info.arg3 = GetOpnd(ea, 2)
        if self.info.arg3 != "":
            inst_elements.append(self.info.arg3)
            nargs += 1
        self.info.nargs = nargs

        if len(inst_elements) >= 1:
            args_str = " "  + ", ".join(inst_elements)
        else:
            args_str = ""
        self.info.inst_str = self.info.opcode + args_str

        try:
            begin_ea = get_entry_ordinal(get_entry(-1))
        except:
            begin_ea = BeginEA()
        if ea == begin_ea:
            self.info.is_root = True
        else:
            self.info.is_root = False

        self.info.address = ea
        self.info.has_address = True

        # node_t
        self.node_id = self._genid()

    def getid(self):
        """Get the node id.

        Returns:
            vsize_t: The id of the node.
        """
        return self.node_id

    def _genid(self):
        """Generate a unique ID for the node.

        Returns:
            vsize_t: The id for the node
        """
        return self.info.address
