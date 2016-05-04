
class JavaHelper(object):

    def __init__(self, spec_lines):
        assert spec_lines is not None, "spec_lines cannot be None"
        self.spec_lines = spec_lines
        self.jfields = []
        self.getter_setters = []

        self.process_spec()

    @staticmethod
    def buildJavaLines(spec_lines):
        jhelper = JavaHelper(spec_lines)
        return jhelper.get_java_lines()

    def process_spec(self):

        for sline in self.spec_lines:
            if sline.startswith('#'):
                continue
            spec_items = sline.split('|')
            spec_items = [x.strip() for x in spec_items]
            self.process_spec_line(spec_items)

    def get_java_lines(self):

        # add tab prefix to each line
        outlines = [ '\t%s' % x for x in self.jfields]
        outlines += self.getter_setters
        return '\n'.join(outlines)

    def format_jfield_for_getset(self, jfield):
        """
        Change first letter of the field name to uppercase
        """
        return jfield[0].upper() + jfield[1:]

    def process_spec_line(self, spec_items):
        assert len(spec_items) in [2, 3],\
            ("The 'spec_items' should have "
             "two or three items, not %s: %s" %\
             (len(spec_items), spec_items))

        db_params = None
        if len(spec_items) == 3:
            jfield, jtype, db_params = spec_items
        else:
            jfield, jtype = spec_items

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

if __name__=='__main__':
    content = open('input/example01.txt')
    #jhelper = JavaHelper(content)
    #print jhelper.get_java_lines()

    print JavaHelper.buildJavaLines(content)
