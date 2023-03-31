from kivy.logger import Logger
from kivy.utils import platform
from jnius import autoclass, PythonJavaClass, java_method

if platform == 'android':
    mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
    Context = autoclass('android.content.Context')
    System = autoclass('java.lang.System')
    CharSequence = autoclass('java.lang.CharSequence')
    PackageManager = autoclass('android.content.pm.PackageManager')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    String = autoclass('java.lang.String')
    NfcAdapter = autoclass('android.nfc.NfcAdapter')
    IntentFilter = autoclass('android.content.IntentFilter')
    PendingIntent = autoclass('android.app.PendingIntent')
    TechList = autoclass('java.lang.String[][]')
    Tag = autoclass('android.nfc.Tag')

class NfcReader(PythonJavaClass):
    __javainterfaces__ = ['android.nfc.NfcAdapter$ReaderCallback']

    def __init__(self, callback):
        super(NfcReader, self).__init__()
        self.callback = callback

    @java_method('(Landroid/nfc/NfcAdapter$Tag;)V')
    def onTagDiscovered(self, tag):
        id_bytes = tag.getId()
        id_hex = ''.join(['{:02x}'.format(x) for x in id_bytes])
        self.callback(id_hex)

class NFCApp(App):

    def build(self):
        if platform == 'android':
            self.nfc_adapter = NfcAdapter.getDefaultAdapter(mActivity)
            if not self.nfc_adapter:
                Logger.info('NFCReader: no NFC adapter found')
                return
            self.pending_intent = PendingIntent.getActivity(mActivity, 0, Intent(mActivity, mActivity.getClass()).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), 0)
            self.intent_filters_array = []
            self.tech_list_array = [
                ['android.nfc.tech.IsoDep'],
                ['android.nfc.tech.NfcA'],
                ['android.nfc.tech.NfcB'],
                ['android.nfc.tech.NfcF'],
                ['android.nfc.tech.NfcV'],
                ['android.nfc.tech.NdefFormatable'],
                ['android.nfc.tech.MifareClassic'],
                ['android.nfc.tech.MifareUltralight'],
            ]
            self.tech_list = TechList(self.tech_list_array)
            self.intent_filters_array.append(IntentFilter(NfcAdapter.ACTION_TECH_DISCOVERED).add)
