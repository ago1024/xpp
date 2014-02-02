from resource_classes import _resource_classes

_templates = {}

_templates['iter_fixed'] = \
"""\
                     xpp::iterator<%s,
                                   %s,
                                   %s_reply_t,
                                   CALLABLE(%s_%s),
                                   CALLABLE(%s_%s_length)>\
"""

_templates['iter_variable'] = \
"""\
                        xpp::iterator<%s,
                                      %s,
                                      %s_reply_t,
                                      %s_iterator_t,
                                      CALLABLE(%s_next),
                                      CALLABLE(%s_sizeof),
                                      CALLABLE(%s_%s_iterator)>\
"""

_templates['list'] = \
"""\
    xpp::generic::list<%s_reply_t,
                       %s
                      >
    %s(void)
    {
      return xpp::generic::list<%s_reply_t,
                                %s
                               >(%s);
    }\
"""

_templates['iter_string'] = \
"""\
xpp::generic::string<
                     %s_reply_t,
                     &%s_%s,
                     &%s_%s_length>\
"""

_templates['string'] = \
"""\
    %s
    %s(void)
    {
      return %s
               (this->get());
    }\
"""

class Accessor(object):
    def __init__(self, is_fixed=False, is_string=False, is_variable=False, \
                 member="", c_type="", return_type="", iter_name="", c_name=""):

        self.is_fixed = is_fixed
        self.is_string = is_string
        self.is_variable = is_variable

        self.member = member
        self.c_type = c_type
        self.return_type = return_type
        self.iter_name = iter_name
        self.c_name = c_name

        self.object_type = self.c_type.replace("xcb_", "").replace("_t", "").upper()

        if self.c_type == "void":
          self.return_type = "Type"
        elif self.object_type in _resource_classes:
          self.return_type = self.member.capitalize()
        else:
          self.return_type = self.c_type

    def __str__(self):
        if self.is_fixed:
            return self.list(self.iter_fixed())
        elif self.is_variable:
            return self.list(self.iter_variable())
        elif self.is_string:
            return self.string()
        else:
            return ""


    def iter_fixed(self):
        return_type = self.return_type

        return _templates['iter_fixed'] \
                % (self.c_type,
                   return_type,
                   self.c_name,
                   self.c_name, self.member,
                   self.c_name, self.member)


    def iter_variable(self):
        return _templates['iter_variable'] \
                % (self.c_type,
                   self.return_type,
                   self.c_name,
                   self.iter_name,
                   self.iter_name,
                   self.iter_name,
                   self.c_name, self.member)


    def list(self, iterator):

        template = "    template<typename Type" if self.c_type == "void" else ""

        # template<typename Children = xcb_window_t>
        if self.object_type in _resource_classes:
          template += ", " if template != "" else "    template<typename "
          template += self.member.capitalize() + " = " + self.c_type

        template += ">\n" if template != "" else ""

        c_tor_params = "m_c, this->get()"

        return template + _templates['list'] \
                % (self.c_name,
                   iterator,
                   self.member,
                   self.c_name,
                   iterator,
                   c_tor_params)

    def string(self):
        string = _templates['iter_string'] \
                % (self.c_name,
                   self.c_name, self.member,
                   self.c_name, self.member)

        return _templates['string'] % (string, self.member, string)