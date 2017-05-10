__author__ = 'bosito7'
__contact__ = 'bosito7@gmail.com'


import logging
import caffe
from caffe import layers as L

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import os
import commands
import subprocess

class consoleBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def message(self, msg):
        print('Terminal command requested')
        print(msg['body'])
        command = msg['body']
        commandOut = commands.getstatusoutput(command)
        msg.reply(commandOut[1]).send()
        #if msg['type'] in ('chat', 'normal'):
        #    msg.reply("Thanks for sending\n%(body)s" % msg).send()

        #sp = subprocess
        #extract_popen = subprocess.Popen('sh ' + command, stdout=sp.PIPE, stderr=sp.STDOUT)
        #for line in extract_popen.stdout:
        #    msg.reply(line).send()


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')

    xmpp = consoleBot('console.chat.bot@gmail.com', 'consolechat')
    xmpp.connect()
    xmpp.process(block=True)