import sys
import os.path
import s_expression
from domain_ast import domain
from domain_codegen import domain_code

def main():
    if len(sys.argv) == 3:
        src = sys.argv[1]
        dst = sys.argv[2]

        self_dir = os.path.dirname(os.path.realpath(__file__))
        domain_std_path = os.path.join(self_dir, 'domain_std.py')

        if not os.path.isfile(domain_std_path):
            print 'Error: Cant find domain_std module.'
            sys.exit(1)

        try:
            s = s_expression.parse(open(src, 'rt').read())
            d = domain.build(s)
            c = domain_code.generate(d, inline_modules=[open(domain_std_path, 'rt')])
        except (s_expression.MalformedExpressionError, s_expression.SyntaxException) as e:
            print 'Error: line=%s column=%s'%(e.pos[0], e.pos[1])
            sys.exit(1)

        with open(dst, 'wt') as f:
            f.write('# Auto-generated with translate_domain.py\n\n')
            f.write(c)

        print 'Done!'
    else:
        print 'translate_domain.py <source> <destination>'

if __name__ == '__main__':
    main()
