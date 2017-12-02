"""
   <!-- <context name="features"> -->
"""

from wirecurly.dialplan import Extension
from wirecurly.dialplan.applications.tools import *
from wirecurly.dialplan.expression import ExpressionField
from wirecurly.dialplan.condition import *
from wirecurly.dialplan.context import Context

class Features:
    @classmethod
    def dx(csl):
        """In call Transfer for phones without a transfer button"""
        ext = Extension('dx')
        cond = Condition(expr=ExpressionField("destination_number", "^dx$"))
        cond.addApplication(Answer())
        cond.addAction("read", val="4 11 'tone_stream://%(10000,0,350,440)' digits ${dx-dtmf-timeout} #")
        cond.addAction("execute_extension", val="is_transfer XML default")
        ext.addCondition(cond)
        return ext
    
    @classmethod
    def att_xfer(cls):
        ext = Extension('att_xfer')
        cond = Condition(expr=ExpressionField("destination_number", "^att_xfer$"))
        cond.addAction("read", val="3 4 'tone_stream://%(10000,0,350,440)' digits 30000 #")
        cond.addAction("set", val="origination_cancel_key=#")
        cond.addAction("att_xfer", val="user/${digits}@${domain_name}")
        ext.addCondition(cond)
        return ext
    
    @classmethod
    def is_transfer(cls):
        ext = Extension('is_transfer')
        cond1 = Condition(expr=ExpressionField(field="destination_number", exp="^is_transfer$"))
        cond2 = Condition(expr=ExpressionField(field="${digits}", exp="^(\d+)$"))
        cond2.addApplication(Transfer("-bleg ${digits} XML ${domain_name}"))
        cond2.addAntiApplication(Eval("cancel transfer"))
        ext.addCondition(cond1)
        ext.addCondition(cond2)
        return ext
    
    @classmethod
    def cf(cls):
        ext = Extension('cf')
        cond = Condition(expr=ExpressionField(field="destination_number", exp="^cf$"))
        cond.addApplication(Answer())
        cond.addApplication(Transfer("-both 30${dialed_extension:2} XML ${domain_name}"))
        ext.addCondition(cond)
        return ext
    
    @classmethod
    def please_hold(cls):
        ext = Extension('please_hold')
        cond = Condition(expr=ExpressionField(field="destination_number", exp="^please_hold$"))
        cond.addApplication(Set("transfer_ringback", "local_stream://moh"))
        cond.addApplication(Answer())
        cond.addApplication(Sleep("1500"))
        cond.addAction("playback", "ivr/ivr-hold_connect_call.wav")
        cond.addApplication(Transfer("$1 XML ${domain_name}"))
        ext.addCondition(cond)
        return ext
    
    @classmethod
    def to_context(cls, context_name):
        context = Context(context_name)
        context.addExternalExtension(cls.dx())
        context.addExternalExtension(cls.att_xfer())
        context.addExternalExtension(cls.is_transfer())
        context.addExternalExtension(cls.cf())
        context.addExternalExtension(cls.please_hold())
        return context
    
"""

    <!--
    <extension name="is_zrtp_secure" continue="true">
      <condition field="${zrtp_secure_media_confirmed}" expression="^true$">
    <action application="sleep" data="1000"/>
    <action application="playback" data="misc/call_secured.wav"/>
    <anti-action application="eval" data="not_secure"/>
      </condition>
    </extension>
    -->
    <!--
    <extension name="is_secure" continue="true">
      < ! - - Only Truly consider it secure if its TLS and SRTP - - > 
      <condition field="${sip_via_protocol}" expression="tls"/>
      <condition field="${rtp_secure_media_confirmed}" expression="^true$">
    <action application="sleep" data="1000"/>
    <action application="playback" data="misc/call_secured.wav"/>
    <anti-action application="eval" data="not_secure"/>
      </condition>
    </extension>
    -->

    <!-- </context> -->
"""