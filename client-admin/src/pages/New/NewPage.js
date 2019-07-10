import React, { PureComponent, Fragment } from 'react';
import ImageWrapper from '@/components/ImageWrapper';
import { ChartCard, MiniBar } from '@/components/Charts';
import { Tooltip, Icon } from 'antd';
import SimpleMDE from 'simplemde';
import marked from 'marked';
import highlight from 'highlight.js';
import 'simplemde/dist/simplemde.min.css';
import styles from './NewPage.less';

const visitData = [
  {
    x: '2017-09-01',
    y: 100,
  },
  {
    x: '2017-09-02',
    y: 120,
  },
  {
    x: '2017-09-03',
    y: 88,
  },
  {
    x: '2017-09-04',
    y: 65,
  },
];



export default class NewPage extends PureComponent {

  componentDidMount() {
    this.smde = new SimpleMDE({
      element: document.getElementById('editor').childElementCount,  
      autofocus: true,
      autosave: true,
      previewRender: function(plainText) {
              return marked(plainText,{
                      renderer: new marked.Renderer(),
                      gfm: true,
                      pedantic: false,
                      sanitize: false,
                      tables: true,
                      breaks: true,
                      smartLists: true,
                      smartypants: true,
                      highlight: function (code) {
                              return highlight.highlightAuto(code).value;
                      }
              });
      },
    })
  }

  render(){
    return (
      <div>
        <ImageWrapper src="https://os.alipayobjects.com/rmsportal/mgesTPFxodmIwpi.png" desc="示意图" />
        <ChartCard
          title="支付笔数"
          action={
            <Tooltip title="支付笔数反应交易质量">
              <Icon type="exclamation-circle-o" />
            </Tooltip>
          }
          total="6,500"
          contentHeight={46}
        >
          <MiniBar height={46} data={visitData} />
        </ChartCard>
        <div title="添加与修改文章" width="1200px">
          <textarea id="editor" style={{ zIndex:100 }} size="large" rows={6} />
        </div>
      </div>
    )
  }
  
};

