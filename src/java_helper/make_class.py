
class JavaHelper(object):

    def __init__(self, spec_lines):
        assert spec_lines is not None, "spec_lines cannot be None"
        self.spec_lines = spec_lines
        self.jfield_names = []
        self.jfields = []
        self.getter_setters = []
        self.json_lines = []

        self.process_spec()

    @staticmethod
    def buildJavaLines(spec_lines):
        jhelper = JavaHelper(spec_lines)
        return jhelper.get_java_lines()

    def process_spec(self):

        for idx, sline in enumerate(self.spec_lines):
            if sline.startswith('#'):
                continue
            spec_items = sline.split('|')
            spec_items = [x.strip() for x in spec_items]
            self.process_spec_line(spec_items, idx)

    def get_java_lines(self, includeJSON=True):

        # add tab prefix to each line
        outlines = [ '\t%s' % x for x in self.jfields]
        outlines += self.getter_setters

        if includeJSON:
            return '\n'.join(outlines) + self.format_json_lines()
        else:
            return '\n'.join(outlines)

    def format_jfield_for_getset(self, jfield):
        """
        Change first letter of the field name to uppercase
        """
        return jfield[0].upper() + jfield[1:]

    def process_spec_line(self, spec_items, idx=None):
        assert len(spec_items) in [2, 3],\
            ("The 'spec_items' should have "
             "two or three items, not %s: %s" %\
             (len(spec_items), spec_items))

        db_params = None
        if len(spec_items) == 3:
            jfield, jtype, db_params = spec_items
        else:
            jfield, jtype = spec_items

        self.jfield_names.append(jfield)

        if db_params:
            for param in db_params.split(','):
                if param == 'pkey':
                    self.jfields.append('@Id')
                    self.jfields.append('@GeneratedValue(strategy = GenerationType.AUTO)')
                elif param == 'unique':
                    self.jfields.append('@Column(nullable=false, unique=true)')
                elif param == 'notnull':
                    self.jfields.append('@Column( nullable=false )')

                if param == 'email':
                    self.jfields.append('@ValidateEmail(message = "Please enter a valid email address.")')

        jdef = "private %s %s;\n" % (jtype, jfield)
        self.jfields.append(jdef)

        #getter_setter = """{0}({1} {2}){""".format('dog', 'apple', 'cat')

        getter_setter = """
    /**
     *  Set {2}
     *  @param {2}
     */
    public void set{0}({1} {2}){{
        this.{2} = {2};
    }}

    /**
     *  Get for {2}
     *  @return {1}
     */
    public {1} get{0}(){{
        return this.{2};
    }}
    """.format(self.format_jfield_for_getset(jfield), jtype, jfield)
        self.getter_setters.append(getter_setter)

        self.add_json_line(jfield, jtype)

    def add_json_line(self, jfield, jtype):
        """
        Add JSON lines
        """

        if jtype == 'boolean':
            jline = '\tjsonData.add("{0}", this.{0});'.format(\
                        jfield)
        else:
            default_val = self.get_json_default_val(jtype)
            jline = ('\n\tif (this.{0}==null){{\n'
                    '\t   jsonData.add("{0}", {1});\n'
                    '\t}}else{{\n'
                    '\t   jsonData.add("{0}", this.{0});\n'
                    '\t}}').format(jfield, default_val)

        self.json_lines.append(jline)


    def get_json_default_val(self, jtype):
        #if jtype == 'boolean':
        #    return 'JsonValue.TRUE'
        if jtype == 'String':
            #return '""'
            return 'JsonValue.NULL';
        elif jtype in ['Long', 'Float', 'Integer']:
            return 'JsonValue.NULL' #'-99'
        else:
            return 'JsonValue.NULL';

    def get_field_names_as_java_list(self):

        attrs = [ '"%s"' % x for x in self.jfield_names]

        return """Arrays.asList(%s);""" % (','.join(attrs))


    def format_json_lines(self):

        json_method = """\npublic String asJSON(){

    // Initialize JSON response
    JsonObjectBuilder jsonData = Json.createObjectBuilder();

    %s

    return jsonData.build().toString();

    }""" % ('\n'.join(self.json_lines))

        return json_method



if __name__=='__main__':
    content = open('input/offset.txt')
    jhelper = JavaHelper(content)
    print jhelper.get_java_lines(includeJSON=False)

    #print JavaHelper.buildJavaLines(content)

    jhelper = JavaHelper(content)
    #print jhelper.get_field_names_as_java_list()
