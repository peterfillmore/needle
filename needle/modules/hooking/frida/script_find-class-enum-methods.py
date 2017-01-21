from core.framework.module import FridaScript


class Module(FridaScript):
    meta = {
        'name': 'Frida Script: find class and enumerate its methods',
        'author': '@LanciniMarco (@MWRLabs)',
        'description': 'Find the target class specified and enumerate its methods',
        'options': (
            ('output', True, False, 'Full path of the output file'),
            ('target_class', "", True, 'Target class, whose methods needs to be enumerated.'),
        ),
    }

    JS = '''\
if(ObjC.available) {
    for(var className in ObjC.classes) {
        if(ObjC.classes.hasOwnProperty(className)) {
            if(className == "%s") {
                console.log("Found target class : " + className);
                console.log("Methods found : ")
                var methods = ObjC.classes.%s.$methods
                for (var i = 0; i < methods.length; i++) {
                    send(JSON.stringify({class:className.toString(), method:methods[i].toString()}));
                }
            }
        }
    }
} else {
    console.log("Objective-C Runtime is not available!");
}
    '''

    # ==================================================================================================================
    # UTILS
    # ==================================================================================================================
    def __init__(self, params):
        FridaScript.__init__(self, params)
        # Setting default output file
        self.options['output'] = self.local_op.build_output_path_for_file("frida_script_enummethods.txt", self)

    # ==================================================================================================================
    # RUN
    # ==================================================================================================================
    def module_run(self):
        # Build the payload string
        target_class = self.options['target_class']
        hook = self.JS % (target_class, target_class)
        # Run payload
        self.run_payload(hook)

    def module_post(self):
        self.print_cmd_output()
